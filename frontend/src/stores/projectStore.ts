import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export interface Project {
  id: number
  title: string
  description: string
  status: 'In Progress' | 'Completed' | 'Draft'
  stepCurrent: number
  stepTotal: number
  date: string
  imageUrl: string
}

const DEFAULT_PROJECTS: Project[] = []

export const useProjectStore = defineStore('project', () => {
  // Load from localStorage or defaults
  let initialProjects = DEFAULT_PROJECTS
  const stored = localStorage.getItem('mdgen-projects')
  
  if (stored) {
    try {
      initialProjects = JSON.parse(stored)
    } catch (e) {
      console.error('Error parsing projects from localStorage', e)
    }
  }

  const projects = ref<Project[]>(initialProjects)

  // Persist changes
  watch(projects, (newVal) => {
    localStorage.setItem('mdgen-projects', JSON.stringify(newVal))
  }, { deep: true })


  // Get next available ID
  const getNextId = () => {
    const maxId = projects.value.reduce((max, p) => Math.max(max, p.id), 0)
    return maxId + 1
  }

  // Create a new project
  const createProject = (title: string, description: string) => {
    const newProject: Project = {
      id: getNextId(),
      title,
      description: description || 'Sin descripción',
      status: 'Draft',
      stepCurrent: 1,
      stepTotal: 5,
      date: new Date().toLocaleDateString('es-ES'),
      imageUrl: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80' // Default placeholder
    }
    
    // Add to beginning of list
    projects.value.unshift(newProject)
    return newProject
  }

  // Update an existing project
  const updateProject = (id: number, updates: Partial<Project>) => {
    const index = projects.value.findIndex(p => p.id === id)
    if (index !== -1) {
      const existingProject = projects.value[index];
      projects.value[index] = { 
        ...existingProject, 
        ...updates 
      } as Project;
      
      // Auto-update status based on step
      if (projects.value[index].stepCurrent === 1) {
        projects.value[index].status = 'Draft'
      } else if (projects.value[index].stepCurrent >= 2 && projects.value[index].stepCurrent <= 4) {
        projects.value[index].status = 'In Progress'
      } else if (projects.value[index].stepCurrent === 5) {
        projects.value[index].status = 'Completed'
      }
    }
  }

  // Get project by ID
  const getProject = (id: number) => {
    return projects.value.find(p => p.id === id)
  }

  return {
    projects,
    createProject,
    updateProject,
    getProject
  }
})

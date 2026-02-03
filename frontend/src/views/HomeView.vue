<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useProjectStore } from '../stores/projectStore'
import StatCard from '../components/StatCard.vue'
import ProjectCard from '../components/ProjectCard.vue'

const router = useRouter()
const projectStore = useProjectStore()
const { projects } = storeToRefs(projectStore)

const isModalOpen = ref(false)
const newProjectForm = ref({
  name: '',
  description: ''
})

const stats = computed(() => {
  const total = projects.value.length
  const inProgress = projects.value.filter(p => p.status === 'In Progress').length
  const completed = projects.value.filter(p => p.status === 'Completed').length
  
  return [
    { title: 'Total Proyectos', count: total, icon: 'video', color: 'blue' },
    { title: 'En Progreso', count: inProgress, icon: 'clock', color: 'orange' },
    { title: 'Completados', count: completed, icon: 'check', color: 'green' },
  ] as const
})

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  newProjectForm.value = { name: '', description: '' }
}

const createProject = () => {
  if (!newProjectForm.value.name.trim()) return
  
  // Use store to create project
  const newProject = projectStore.createProject(
    newProjectForm.value.name, 
    newProjectForm.value.description
  )
  
  // Navigate to step 1
  router.push({
    path: `/project/${newProject.id}`,
    // Still passing query params for fallback/initial load if view relies on them
    query: { 
      name: newProject.title,
      desc: newProject.description
    }
  })
  closeModal()
}
</script>

<template>
  <div class="home-container">
    <!-- Header -->
    <header class="app-header">
      <div class="header-left">
        <div class="logo-box">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M15.6 11.6L22 7v10l-6.4-4.5v-1z" />
            <path d="M4 5h9a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V7c0-1.1.9-2 2-2z" />
          </svg>
        </div>
        <div>
          <h1 class="app-title">MDGen</h1>
          <p class="app-subtitle">Plataforma de generación de videos instruccionales</p>
        </div>
      </div>
      <div class="header-right">
        <!-- "Ver Diagrama" button purposefully omitted as requested -->
        <button class="btn-primary" @click="openModal">
          <span>+ Nuevo Proyecto</span>
        </button>
      </div>
    </header>

    <!-- Stats Row -->
    <section class="stats-section">
      <StatCard
        v-for="stat in stats"
        :key="stat.title"
        :title="stat.title"
        :count="stat.count"
        :iconType="stat.icon"
        :color="stat.color"
      />
    </section>

    <!-- Projects Section -->
    <section class="projects-section">
      <h2 class="section-title">Mis Proyectos</h2>
      <div class="projects-grid">
<ProjectCard 
          v-for="project in projects" 
          :key="project.id" 
          v-bind="project"
          @click="$router.push(`/project/${project.id}`)"
        />
      </div>
    </section>

    <!-- Create Project Modal -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3 class="modal-title">Nuevo Proyecto</h3>
          <button class="close-btn" @click="closeModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label for="p-name">Nombre del Proyecto</label>
            <input 
              id="p-name" 
              type="text" 
              v-model="newProjectForm.name" 
              placeholder="Ej: Curso de Python 101"
              autofocus
            >
          </div>
          <div class="form-group">
            <label for="p-desc">Descripción (Opcional)</label>
            <textarea 
              id="p-desc" 
              v-model="newProjectForm.description" 
              placeholder="Breve descripción del objetivo..."
              rows="3"
            ></textarea>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" @click="closeModal">Cancelar</button>
          <button class="btn-primary" @click="createProject" :disabled="!newProjectForm.name">
            Crear Proyecto
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-card {
  background-color: white;
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  animation: modalPop 0.2s ease-out;
}

@keyframes modalPop {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  border-radius: 4px;
  display: flex;
}

.close-btn:hover {
  background-color: #f3f4f6;
  color: #111827;
}

.modal-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.form-group input,
.form-group textarea {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.9375rem;
  outline: none;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.modal-footer {
  padding: 20px 24px;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-secondary {
  padding: 10px 16px;
  background-color: white;
  border: 1px solid #d1d5db;
  color: #374151;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-secondary:hover {
  background-color: #f3f4f6;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Existing Styles */

.home-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 24px;
}

/* Header */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 48px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-box {
  width: 48px;
  height: 48px;
  background-color: #2563eb;
  color: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
}

.app-subtitle {
  color: #6b7280;
  font-size: 0.875rem;
}

.btn-primary {
  background-color: #0f172a; /* Black/Dark Info */
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary:hover {
  background-color: #1e293b;
}

/* Stats */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

/* Projects */
.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 24px;
  color: #111827;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 32px;
}

@media (max-width: 768px) {
  .app-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .header-right {
    width: 100%;
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
  }
}
</style>

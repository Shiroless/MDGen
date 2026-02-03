<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  currentStep: number;
}>();

const emit = defineEmits(['update:step']);

const steps = [
  { id: 1, label: 'Desarrollo LLM', icon: 'message', color: 'purple' },
  { id: 2, label: 'Slides & Script', icon: 'presentation', color: 'emerald' },
  { id: 3, label: 'PowerPoint', icon: 'monitor', color: 'orange' },
  { id: 4, label: 'Video Avatar', icon: 'video', color: 'rose' },
  { id: 5, label: 'Exportar', icon: 'upload', color: 'cyan' },
] as const;

// Helper to get class for step circle based on state
const getStepClass = (stepId: number, color: string) => {
  if (stepId < props.currentStep) {
    return 'is-completed';
  } else if (stepId === props.currentStep) {
    return `is-active color-${color}`;
  } else {
    return `is-future color-${color}`;
  }
};
</script>

<template>
  <div class="stepper-wrapper">
    <!-- Pipeline Card -->
    <div class="pipeline-card">
      <h2 class="pipeline-title">Pipeline de Generación</h2>
      
      <div class="steps-container">
        <div 
          v-for="(step, index) in steps" 
          :key="step.id"
          class="step-item"
        >
          <!-- Connecting Line -->
          <div v-if="index < steps.length - 1" class="step-line"></div>

          <button 
            class="step-button"
            @click="emit('update:step', step.id)"
          >
            <div 
              class="step-circle" 
              :class="getStepClass(step.id, step.color)"
            >
              <!-- Completed Check Icon -->
              <svg v-if="step.id < currentStep" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              
              <!-- Regular Icons -->
              <template v-else>
                <!-- Message -->
                <svg v-if="step.icon === 'message'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                <!-- Presentation -->
                <svg v-if="step.icon === 'presentation'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h20"/><path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/><path d="m9 22 3-3 3 3"/><path d="M8 7h8"/></svg>
                <!-- Monitor -->
                <svg v-if="step.icon === 'monitor'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
                <!-- Video -->
                <svg v-if="step.icon === 'video'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 8-6 4 6 4V8Z"/><rect x="2" y="6" width="14" height="12" rx="2" ry="2"/></svg>
                <!-- Upload -->
                <svg v-if="step.icon === 'upload'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              </template>
            </div>
            
            <div class="step-info">
              <span class="step-label">{{ step.label }}</span>
              <span class="step-sub">Paso {{ step.id }}</span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Navigation Pills -->
    <div class="pills-container">
      <div class="pills-track">
        <button 
          v-for="step in steps" 
          :key="`pill-${step.id}`"
          class="step-pill"
          :class="{ 'active': currentStep === step.id }"
          @click="emit('update:step', step.id)"
        >
          Paso {{ step.id }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stepper-wrapper {
  margin-bottom: 32px;
}

/* Pipeline Card */
.pipeline-card {
  background-color: white;
  border-radius: 16px;
  padding: 32px 48px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* Subtle shadow like image */
  border: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.pipeline-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 40px;
}

.steps-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  position: relative;
  width: 100%;
}

.step-item {
  position: relative;
  flex: 1;
  display: flex;
  justify-content: center;
}

/* Connecting Line logic might need adjustment but simpler is better */
/* We need lines BETWEEN items, not across all. flex:1 helps spacing */

.step-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 10;
  width: 100%; /* Ensure it takes full width of item for centering */
}

.step-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.step-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 4px;
}

.step-label {
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
}

.step-sub {
  font-size: 0.75rem;
  color: #9ca3af;
}

/* Colors & States */

/* Completed State - Always Green Check */
.is-completed {
  background-color: #22c55e; /* Green-500 */
  color: white;
  border-color: #22c55e;
}

/* Active State - Solid Color */
.is-active {
  color: white;
  transform: scale(1.1);
  box-shadow: 0 0 0 4px rgba(0,0,0,0.05);
}

.is-active.color-purple { background-color: #a855f7; border-color: #a855f7; }
.is-active.color-emerald { background-color: #10b981; border-color: #10b981; }
.is-active.color-orange { background-color: #f97316; border-color: #f97316; }
.is-active.color-rose { background-color: #f43f5e; border-color: #f43f5e; }
.is-active.color-cyan { background-color: #06b6d4; border-color: #06b6d4; }

/* Future/Inactive State - Light BG, Colored Icon */
.is-future {
  border: 2px solid transparent;
}

.is-future.color-purple { background-color: #f3e8ff; color: #a855f7; }
.is-future.color-emerald { background-color: #d1fae5; color: #10b981; }
.is-future.color-orange { background-color: #ffedd5; color: #f97316; }
.is-future.color-rose { background-color: #ffe4e6; color: #f43f5e; }
.is-future.color-cyan { background-color: #cffafe; color: #06b6d4; }

/* Pills Navigation */
.pills-container {
  width: 100%;
}

.pills-track {
  background-color: #e5e7eb; /* Light Gray Track */
  padding: 4px;
  border-radius: 999px;
  display: flex;
  width: 100%;
  gap: 4px;
}

.step-pill {
  flex: 1;
  padding: 8px 0; /* Remove horizontal padding, rely on flex */
  border-radius: 999px;
  border: none;
  background: transparent;
  color: #6b7280;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.step-pill.active {
  background-color: white;
  color: #111827;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.step-pill:hover:not(.active) {
  color: #374151;
}

/* Connecting Lines - Hard to get perfect flexibly, but roughly: */
/* We can use a pseudo element on step-item */
</style>

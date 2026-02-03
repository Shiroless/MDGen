<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title: string
  description: string
  status: 'In Progress' | 'Draft' | 'Completed'
  stepCurrent?: number
  stepTotal?: number
  date: string
  imageUrl?: string
}>()

const statusLabel = computed(() => {
  switch (props.status) {
    case 'In Progress':
      return 'En Progreso'
    case 'Draft':
      return 'Borrador'
    case 'Completed':
      return 'Completado'
    default:
      return props.status
  }
})

const statusClass = computed(() => {
  switch (props.status) {
    case 'In Progress':
      return 'badge-progress'
    case 'Draft':
      return 'badge-draft'
    case 'Completed':
      return 'badge-completed'
    default:
      return 'badge-default'
  }
})

const progressPercent = computed(() => {
  if (!props.stepCurrent || !props.stepTotal) return 0
  return (props.stepCurrent / props.stepTotal) * 100
})
</script>

<template>
  <div class="project-card">
    <div
      class="card-image"
      :style="{ backgroundImage: imageUrl ? `url(${imageUrl})` : 'background-color: #e5e7eb' }"
    >
      <span :class="['status-badge', statusClass]">{{ statusLabel }}</span>
    </div>

    <div class="card-content">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-desc">{{ description }}</p>

      <div class="card-footer">
        <div class="progress-info">
          <span v-if="stepTotal">Paso {{ stepCurrent }} de {{ stepTotal }}</span>
          <span v-else></span>
          <!-- Spacer -->
          <span class="date">{{ date }}</span>
        </div>

        <div class="progress-bar-bg" v-if="stepTotal">
          <div class="progress-bar-fill" :style="{ width: `${progressPercent}%` }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.project-card {
  background-color: var(--card-bg);
  border-radius: 16px;
  overflow: hidden;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.card-image {
  height: 160px;
  background-size: cover;
  background-position: center;
  position: relative;
  background-color: #374151; /* Fallback dark gray */
}

/* Fallback pattern if no image */
.card-image::before {
  content: '';
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    rgba(0, 0, 0, 0.1) 25%,
    transparent 25%,
    transparent 50%,
    rgba(0, 0, 0, 0.1) 50%,
    rgba(0, 0, 0, 0.1) 75%,
    transparent 75%,
    transparent
  );
  background-size: 20px 20px;
  opacity: 0.1;
}

.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
}

.badge-progress {
  background-color: rgba(219, 234, 254, 0.9); /* Blue-100 */
  color: #1e40af; /* Blue-800 */
}

.badge-draft {
  background-color: rgba(254, 243, 199, 0.9); /* Amber-100 */
  color: #92400e; /* Amber-800 */
}

.badge-completed {
  background-color: rgba(209, 250, 229, 0.9); /* Emerald-100 */
  color: #065f46; /* Emerald-800 */
}

.card-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-color);
}

.card-desc {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 24px;
  line-height: 1.4;
  flex-grow: 1;
}

.card-footer {
  margin-top: auto;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 8px;
  font-weight: 500;
}

.progress-bar-bg {
  height: 6px;
  background-color: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #2563eb;
  border-radius: 3px;
}
</style>

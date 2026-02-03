<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title: string
  count: number | string
  iconType: 'video' | 'clock' | 'check'
  color: 'blue' | 'orange' | 'green'
}>()

const colorClass = computed(() => {
  return `icon-bg-${props.color}`
})
</script>

<template>
  <div class="stat-card">
    <div class="stat-info">
      <span class="stat-title">{{ title }}</span>
      <strong class="stat-count">{{ count }}</strong>
    </div>
    <div :class="['stat-icon', colorClass]">
      <!-- Video Icon -->
      <svg
        v-if="iconType === 'video'"
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
        <path d="M23 7l-7 5 7 5V7z" />
        <rect x="1" y="5" width="15" height="14" rx="2" ry="2" />
      </svg>
      <!-- Clock Icon -->
      <svg
        v-if="iconType === 'clock'"
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
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>
      <!-- Check Icon -->
      <svg
        v-if="iconType === 'check'"
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
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22 4 12 14.01 9 11.01" />
      </svg>
    </div>
  </div>
</template>

<style scoped>
.stat-card {
  background-color: var(--card-bg);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-title {
  color: #6b7280; /* Gray-500 */
  font-size: 0.875rem;
  font-weight: 500;
}

.stat-count {
  color: var(--text-color);
  font-size: 1.875rem;
  font-weight: 700;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-bg-blue {
  background-color: #dbeafe; /* Blue-100 */
  color: #2563eb; /* Blue-600 */
}

.icon-bg-orange {
  background-color: #ffedd5; /* Orange-100 */
  color: #ea580c; /* Orange-600 */
}

.icon-bg-green {
  background-color: #d1fae5; /* Emerald-100 */
  color: #059669; /* Emerald-600 */
}
</style>

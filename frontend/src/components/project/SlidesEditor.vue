<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';

const slides = ref<{
  id: number
  title: string
  points: string[]
  script: string
}[]>([])

// Separate state for Accordion (Left) and Preview (Right)
const expandedSlideIndex = ref(-1); // Start collapsed
const previewSlideIndex = ref(0); // Always start with first slide

const showDeleteConfirm = ref(false);
const slideToDeleteId = ref<number | null>(null);

// Editing State
const editingSlideId = ref<number | null>(null);
const editingData = ref({
  title: '',
  pointsText: '',
  script: ''
});

// Computed for the currently PREVIEWED slide
const previewSlide = computed(() => {
  if (previewSlideIndex.value === -1 || !slides.value[previewSlideIndex.value]) return null;
  return slides.value[previewSlideIndex.value];
});

const toggleSlideAccordion = (index: number) => {
  if (editingSlideId.value !== null) return; // Prevent toggling while editing
  
  if (expandedSlideIndex.value === index) {
    expandedSlideIndex.value = -1; // Collapse
  } else {
    expandedSlideIndex.value = index; // Expand
    // Optional: Sync preview when clicking accordion? User asked for independent navigation, but usually clicking "Edit" implies previewing.
    // Let's keep them separate as requested, but maybe sync on edit?
    // For now, adhere strictly to "preview default 0 + arrows".
  }
};

const nextPreview = () => {
  if (previewSlideIndex.value < slides.value.length - 1) {
    previewSlideIndex.value++;
  }
};

const prevPreview = () => {
  if (previewSlideIndex.value > 0) {
    previewSlideIndex.value--;
  }
};

const addSlide = () => {
  const newId = Math.max(0, ...slides.value.map(s => s.id)) + 1;
  const newSlide = {
    id: newId,
    title: 'Nueva Transparencia',
    points: ['Punto 1', 'Punto 2'],
    script: 'Escribe aquí el guion para esta diapositiva...'
  };
  slides.value.push(newSlide);
  
  // Expand and start editing the new slide
  const newIndex = slides.value.length - 1;
  expandedSlideIndex.value = newIndex;
  // Also jump preview to new slide so user sees what they are adding
  previewSlideIndex.value = newIndex;
  
  nextTick(() => {
    handleEdit(newSlide);
  });
};

const handleEdit = (slide: typeof slides.value[0]) => {
  editingSlideId.value = slide.id;
  editingData.value = {
    title: slide.title,
    pointsText: slide.points.join('\n'),
    script: slide.script
  };
  // Sync preview to the slide being edited
  const index = slides.value.findIndex(s => s.id === slide.id);
  if (index !== -1) previewSlideIndex.value = index;
};

const saveEdit = () => {
  if (editingSlideId.value === null) return;
  
  const points = editingData.value.pointsText
    .split('\n')
    .map(p => p.trim())
    .filter(p => p.length > 0);

  const slideIndex = slides.value.findIndex(s => s.id === editingSlideId.value);
  if (slideIndex !== -1) {
    const existingSlide = slides.value[slideIndex];
    if (!existingSlide) return;
    slides.value[slideIndex] = {
      id: existingSlide.id,
      title: editingData.value.title,
      points: points,
      script: editingData.value.script
    };
  }
  
  editingSlideId.value = null;
};

const cancelEdit = () => {
  editingSlideId.value = null;
};

const requestDelete = (id: number) => {
  slideToDeleteId.value = id;
  showDeleteConfirm.value = true;
};

const confirmDelete = () => {
  if (slideToDeleteId.value !== null) {
    const index = slides.value.findIndex(s => s.id === slideToDeleteId.value);
    if (index !== -1) {
      slides.value.splice(index, 1);
      expandedSlideIndex.value = -1;
      // Adjust preview index if needed
      if (previewSlideIndex.value >= slides.value.length) {
        previewSlideIndex.value = Math.max(0, slides.value.length - 1);
      }
    }
  }
  showDeleteConfirm.value = false;
  slideToDeleteId.value = null;
};

const cancelDelete = () => {
  showDeleteConfirm.value = false;
  slideToDeleteId.value = null;
};

const downloadJson = () => {
  const data = JSON.stringify({ slides: slides.value }, null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'slides_content.json';
  a.click();
  URL.revokeObjectURL(url);
};
</script>

<template>
  <div class="slides-editor">
    <div class="step-header">
      <div class="header-left">
        <div class="step-icon-box">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h20"/><path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/><path d="m9 22 3-3 3 3"/><path d="M8 7h8"/></svg>
        </div>
        <div>
          <h2 class="step-title">Paso 2: Slides & Script</h2>
          <p class="step-desc">Organiza el contenido en transparencias y genera el guion que dirá el avatar. Los contenidos se mantienen en formato plano (Markdown/JSON).</p>
        </div>
      </div>
      <button class="btn-dark" @click="downloadJson">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        Extraer JSON
      </button>
    </div>

    <div class="editor-grid">
      <!-- Left Column: List -->
      <div class="slides-list-col">
        <div class="list-header">
          <span class="list-title">Transparencias ({{ slides.length }})</span>
          <button class="btn-sm-outline" @click="addSlide">+ Añadir</button>
        </div>
        
        <div class="slides-accordion">
          <div v-if="slides.length === 0" class="empty-list-state">
            <p>No hay transparencias. Añade una para empezar.</p>
          </div>
          <div 
            v-for="(slide, index) in slides" 
            :key="slide.id"
            class="slide-item"
            :class="{ 'active': expandedSlideIndex === index }"
            @click="toggleSlideAccordion(index)"
          >
            <!-- Header -->
            <div class="slide-header">
              <div class="slide-item-content">
                <span class="slide-number">{{ index + 1 }}</span>
                <!-- Read Mode Title -->
                <span v-if="editingSlideId !== slide.id" class="slide-item-title">{{ slide.title }}</span>
                <!-- Edit Mode Title Input -->
                <input 
                  v-else 
                  type="text" 
                  v-model="editingData.title"
                  class="edit-input-title"
                  @click.stop
                  placeholder="Título de la transparencia"
                >
              </div>
              <svg v-if="editingSlideId !== slide.id" class="chevron" :class="{ 'rotated': expandedSlideIndex === index }" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
            </div>

            <!-- Expanded Details -->
            <transition name="accordion">
              <div v-show="expandedSlideIndex === index" class="slide-details">
                
                <!-- READ MODE Content -->
                <template v-if="editingSlideId !== slide.id">
                  <div class="detail-section">
                    <span class="detail-label">Contenido de la Transparencia</span>
                    <div class="detail-box">
                      <ul class="detail-list">
                        <li v-for="point in slide.points" :key="point">{{ point }}</li>
                      </ul>
                    </div>
                  </div>

                  <div class="detail-section">
                    <span class="detail-label">Guion del Narrador</span>
                    <div class="detail-box">
                      <p class="detail-text">{{ slide.script }}</p>
                    </div>
                  </div>

                  <div class="slide-actions">
                    <button class="action-btn edit" @click.stop="handleEdit(slide)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                      Editar
                    </button>
                    <button class="action-btn delete" @click.stop="requestDelete(slide.id)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                      Eliminar
                    </button>
                  </div>
                </template>

                <!-- EDIT MODE Content -->
                <template v-else>
                  <div class="detail-section" @click.stop>
                    <span class="detail-label">Contenido (un punto por línea)</span>
                    <textarea 
                      v-model="editingData.pointsText"
                      class="edit-textarea points-area"
                      rows="4"
                      placeholder="- Punto 1&#10;- Punto 2"
                    ></textarea>
                  </div>

                  <div class="detail-section" @click.stop>
                    <span class="detail-label">Guion del Narrador</span>
                    <textarea 
                      v-model="editingData.script"
                      class="edit-textarea script-area"
                      rows="4"
                      placeholder="Escribe el guion aquí..."
                    ></textarea>
                  </div>

                  <div class="slide-actions" @click.stop>
                    <button class="action-btn save" @click="saveEdit">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                      Guardar
                    </button>
                    <button class="action-btn cancel" @click="cancelEdit">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                      Cancelar
                    </button>
                  </div>
                </template>

              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- Right Column: Preview -->
      <div class="slide-preview-col">
        <div class="list-header">
          <span class="list-title">Vista Previa</span>
          <!-- Pagination Controls -->
           <div class="preview-nav">
             <button class="nav-btn" @click="prevPreview" :disabled="previewSlideIndex <= 0">
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
             </button>
             <span class="nav-info">{{ slides.length > 0 ? previewSlideIndex + 1 : 0 }} / {{ slides.length }}</span>
             <button class="nav-btn" @click="nextPreview" :disabled="previewSlideIndex >= slides.length - 1">
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
             </button>
           </div>
        </div>

        <div class="preview-card" v-if="previewSlide">
          <div class="slide-visual">
            <span class="slide-visual-number">SLIDE {{ previewSlideIndex + 1 }} / {{ slides.length }}</span>
            <h3 class="slide-visual-title">{{ editingSlideId === previewSlide.id ? editingData.title : previewSlide.title }}</h3>
            <ul class="slide-visual-points">
              <!-- If editing current previewed slide, show live edit data -->
              <template v-if="editingSlideId === previewSlide.id">
                 <li v-for="point in editingData.pointsText.split('\n').filter(p=>p.trim())" :key="point">{{ point }}</li>
              </template>
              <template v-else>
                 <li v-for="point in previewSlide.points" :key="point">{{ point }}</li>
              </template>
            </ul>
          </div>

          <div class="script-box">
            <h4 class="script-label">GUION DEL NARRADOR:</h4>
            <p class="script-text">{{ editingSlideId === previewSlide.id ? editingData.script : previewSlide.script }}</p>
          </div>
        </div>

        <!-- Empty Preview State -->
        <div class="preview-card empty" v-else>
          <div class="slide-visual empty-visual">
            <p class="empty-text">Sin transparencias</p>
          </div>
          <div class="script-box">
            <h4 class="script-label">GUION DEL NARRADOR:</h4>
            <p class="script-text min-h-text"></p>
          </div>
        </div>
      </div>
    </div>

    <!-- ... (Delete Modal remains the same) ... -->
    <div v-if="showDeleteConfirm" class="modal-overlay">
      <div class="modal-card">
        <h3 class="modal-title">¿Eliminar transparencia?</h3>
        <p class="modal-desc">Esta acción no se puede deshacer. ¿Estás seguro de que quieres continuar?</p>
        <div class="modal-actions">
          <button class="modal-btn cancel" @click="cancelDelete">Cancelar</button>
          <button class="modal-btn confirm" @click="confirmDelete">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ... (keep existing styles) ... */

/* Preview Navigation */
.preview-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 2px;
}

.nav-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  color: #374151;
}

.nav-btn:hover:not(:disabled) {
  background-color: #f3f4f6;
}

.nav-btn:disabled {
  color: #d1d5db;
  cursor: not-allowed;
}

.nav-info {
  font-size: 0.75rem;
  font-weight: 600;
  color: #4b5563;
  min-width: 40px;
  text-align: center;
}

/* ... (rest of styles) ... */

/* Inputs for Edit Mode */
.edit-input-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #111827;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  padding: 4px 8px;
  width: 100%;
  outline: none;
}

.edit-input-title:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

.edit-textarea {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 0.875rem;
  font-family: inherit;
  color: #374151;
  resize: vertical;
  outline: none;
  background-color: white;
}

.edit-textarea:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

.action-btn.save {
  background-color: #10b981;
  color: white;
  border-color: #10b981;
}

.action-btn.save:hover {
  background-color: #059669;
}

.action-btn.cancel {
  color: #4b5563;
}

.accordion-enter-active,
.accordion-leave-active {
  transition: max-height 0.3s ease-out, opacity 0.3s ease, padding-bottom 0.3s ease;
  max-height: 800px; /* Increased for edit mode space */
  overflow: hidden;
}

.accordion-enter-from,
.accordion-leave-to {
  max-height: 0;
  opacity: 0;
  padding-bottom: 0;
}

.slide-details {
  padding: 0 16px 16px 16px;
  border-top: none;
}

.detail-section {
  margin-bottom: 16px;
}

.detail-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #4b5563; /* Gray-600 */
  margin-bottom: 8px;
}

.detail-box {
  background-color: #f3f4f6; /* Gray-100 as per image */
  border-radius: 8px;
  padding: 12px 16px;
}

.detail-list {
  padding-left: 16px;
  margin: 0;
  list-style-type: none; /* User image shows bullets manually like '- ' or styled */
}

.detail-list li {
  position: relative;
  margin-bottom: 4px;
  font-size: 0.875rem;
  color: #1f2937;
}

.detail-list li::before {
  content: '- ';
  margin-right: 4px;
  font-weight: bold;
}

.detail-text {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.5;
}

.slide-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 600;
  background-color: white;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.edit {
  color: #1f2937;
}

.action-btn.delete {
  color: #dc2626; /* Red-600 */
  border-color: #fee2e2;
  background-color: #fff1f2;
}

.action-btn:hover {
  filter: brightness(0.95);
}

.slides-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative; /* For modal positioning context if needed, though fixed is better */
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  background-color: white;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
}

.header-left {
  display: flex;
  gap: 16px;
}

.step-icon-box {
  width: 48px;
  height: 48px;
  background-color: #d1fae5; /* Emerald-100 */
  color: #10b981; /* Emerald-500 */
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 4px;
}

.step-desc {
  color: #6b7280;
  font-size: 0.9375rem;
  max-width: 600px;
  line-height: 1.5;
}

.btn-dark {
  padding: 8px 16px;
  background-color: #000;
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  border: none;
  cursor: pointer;
}

.btn-dark:hover {
  opacity: 0.9;
}

.editor-grid {
  display: grid;
  grid-template-columns: 450px 1fr; /* Increased width for better readabilty of details */
  gap: 32px;
  align-items: start;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.list-title {
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
}

.btn-sm-outline {
  padding: 4px 12px;
  border: 1px solid #d1d5db;
  background-color: white;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
}

.slides-accordion {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.slide-item {
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
}

.slide-item:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.slide-item.active {
  border-color: #d1d5db;
}

/* Header part of item */
.slide-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slide-item-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1; /* Allow content to grow for input */
}

.slide-number {
  background-color: #f3f4f6;
  color: #6b7280;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
  flex-shrink: 0;
}

.slide-item-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #111827;
}

.chevron {
  color: #9ca3af;
  transition: transform 0.2s;
}

.chevron.rotated {
  transform: rotate(180deg);
}

.preview-card {
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.slide-visual {
  background-color: #f8fafc;
  padding: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-height: 300px;
  justify-content: center;
  border-bottom: 1px solid #e5e7eb;
}

.slide-visual-number {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-bottom: 16px;
  letter-spacing: 0.05em;
}

.slide-visual-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 24px;
}

.slide-visual-points {
  list-style-type: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.slide-visual-points li {
  color: #4b5563;
  font-size: 1rem;
}

.slide-visual-points li::before {
  content: '- ';
  color: #d1d5db;
}

.script-box {
  padding: 24px;
  background-color: white;
}

.script-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 8px;
  text-transform: uppercase;
}

.script-text {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.6;
}

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
}

.modal-card {
  background-color: white;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}

.modal-desc {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 24px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.modal-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.modal-btn.cancel {
  background-color: white;
  border: 1px solid #d1d5db;
  color: #374151;
}

.modal-btn.cancel:hover {
  background-color: #f3f4f6;
}

.modal-btn.confirm {
  background-color: #dc2626;
  color: white;
}

.modal-btn.confirm:hover {
  background-color: #b91c1c;
}

/* Empty States */
.empty-list-state {
  padding: 32px;
  text-align: center;
  color: #9ca3af;
  border: 1px dashed #e5e7eb;
  border-radius: 8px;
  background-color: #f9fafb;
}

.preview-card.empty {
  opacity: 0.7;
}

.empty-visual {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
}

.empty-text {
  color: #9ca3af;
  font-size: 1.125rem;
  font-weight: 500;
}

.min-h-text {
  min-height: 1.5em; /* Ensure script box has some height even if empty */
}
</style>

<template>
  <div class="modal-container">
    <div class="modal-content">
      <button @click="$emit('close-modal')" class="close-button">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-8 h-8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalView'
};
</script>

<style scoped>
.modal-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 400px;
  height: 600px;
  background-color: white;
  z-index: 1000;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.modal-content {
  position: relative;
  height: 100%;
  overflow-y: auto;
}
.close-button {
  position: absolute;
  top: 10px; 
  right: 10px; 
  z-index: 1001; 
  background: white; 
  border-radius: 50%;
  padding: 8px; 
}
.close-button svg {
  width: 24px; 
  height: 24px; 
}
</style>

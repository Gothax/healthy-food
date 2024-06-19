<template>
    <div class="email-form">
      <h2>불량 문의</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="phone_number">전화번호:</label>
          <input type="text" v-model="form.phone_number" id="phone_number" name="phone_number" required />
        </div>
        <div>
          <label for="product_number">제품 번호:</label>
          <input type="text" v-model="form.product_number" id="product_number" name="product_number" required />
        </div>
        <div>
          <label for="product_name">제품 이름:</label>
          <input type="text" v-model="form.product_name" id="product_name" name="product_name" required />
        </div>
        <div>
          <label for="text">문의 내용:</label>
          <textarea v-model="form.text" id="text" name="text" required></textarea>
        </div>
        <div>
          <label for="file">첨부 파일:</label>
          <div class="file-upload">
            <input type="file" @change="handleFileUpload" id="file" ref="fileInput" required />
            <button type="button" @click="triggerFileInput">파일 선택</button>
          </div>
          <span v-if="form.file">{{ form.file.name }}</span>
        </div>
        <div v-if="previewUrl" class="preview-container">
          <img :src="previewUrl" alt="File Preview" class="preview-image"/>
        </div>
        <button type="submit" :disabled="isSending">{{ isSending ? '보내는 중...' : '보내기' }}</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    data() {
      return {
        form: {
          phone_number: '',
          product_number: '',
          product_name: '',
          text: '',
          file: null as File | null,
        },
        previewUrl: null as string | null,
        isSending: false, //
      };
    },
    methods: {
      handleFileUpload(event: Event) {
        const target = event.target as HTMLInputElement;
        const file = target.files ? target.files[0] : null;
        this.form.file = file;
        if (file) {
          const reader = new FileReader();
          reader.onload = (e: ProgressEvent<FileReader>) => {
            if (e.target) {
              this.previewUrl = e.target.result as string;
            }
          };
          reader.readAsDataURL(file);
        }
      },
      triggerFileInput() {
        (this.$refs.fileInput as HTMLInputElement).click();
      },
      async submitForm() {
        this.isSending = true; //
        const formData = new FormData();
        formData.append('phone_number', this.form.phone_number);
        formData.append('product_number', this.form.product_number);
        formData.append('product_name', this.form.product_name);
        formData.append('text', this.form.text);
        if (this.form.file) {
          formData.append('file', this.form.file);
        }
  
        try {
          const response = await fetch('http://127.0.0.1:8000/api/mail/', {
            method: 'POST',
            body: formData,
          });
  
          if (response.ok) {
            const data = await response.json();
            this.$emit('emailSent', data.message);
          } 
        } finally {
          this.isSending = false;
        }
      },
    },
  });
  </script>
  
  <style scoped>
  .email-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .email-form form {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .email-form label {
    font-weight: bold;
  }
  
  .email-form input,
  .email-form textarea {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 5px;
    width: 100%;
  }
  
  .email-form button {
    padding: 10px;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .email-form button:hover {
    background-color: #0056b3;
  }
  
  .file-upload {
    display: flex;
    align-items: center;
  }
  
  .file-upload input[type="file"] {
    display: none;
  }
  
  .file-upload button {
    padding: 8px 12px;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .file-upload button:hover {
    background-color: #0056b3;
  }
  
  .preview-container {
    margin-top: 10px;
  }
  
  .preview-image {
    max-width: 200px;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  </style>
  
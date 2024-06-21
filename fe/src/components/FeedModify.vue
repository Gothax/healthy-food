<template>
  <form v-on:submit.prevent="submitForm" method="post">
    <div class="p-4">
      <textarea
        v-model="body"
        class="p-4 w-full bg-gray-100 rounded-lg"
        placeholder="Body"
      ></textarea>

      <div id="preview" v-if="urls.length">
        <div v-for="(url, index) in urls" :key="index" class="image-card">
          <img :src="url" class="w-[100px] mt-3 rounded-xl" />
          <button @click="removeUrl(index)" type="button" class="remove-button">
            <img src="@/assets/X.png" />
          </button>
        </div>
      </div>
    </div>

    <div class="image-grid" v-if="attachments.length || urls.length">
        <div v-for="(attachment, index) in filteredAttachments" :key="attachment.id" class="image-card">
            <img :src="attachment.get_image" class="w-full rounded-xl" />
            <button @click="removeAttachment(index)" type="button" class="remove-button">
            <img src="@/assets/X.png" />
            </button>
        </div>
        <div v-for="(url, index) in urls" :key="index" class="image-card">
            <img :src="url" class="w-full rounded-xl" />
            <button @click="removeUrl(index)" type="button" class="remove-button">
            <img src="@/assets/X.png" />
            </button>
        </div>
    </div>

    <div class="p-4 border-t border-gray-100 flex justify-between">
      <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
        <input type="file" ref="file" @change="onFileChange" multiple />
        Attach images
      </label>
      <button
        type="submit"
        class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
      >
        Done
      </button>
    </div>
  </form>
</template>

<script>
import axios from "axios";

export default {
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
    body: this.post.body || "",
      attachments: this.post.attachments || [],
      urls: [],
      attachmentsToRemove: [],
      newFiles: [],  // 새로운 파일을 추적하기 위해 추가
    };
  },
  computed: {
    filteredAttachments() {
      // attachmentsToRemove에 포함되지 않은 attachments만 반환
      return this.attachments.filter(
        (attachment) => !this.attachmentsToRemove.includes(attachment.id)
      );
    },
  },
  methods: {
    onFileChange(e) {
      const files = e.target.files;
      this.urls = Array.from(files).map((file) => URL.createObjectURL(file));
      this.newFiles = Array.from(files);
    },
    removeAttachment(index) {
        this.attachmentsToRemove.push(this.filteredAttachments[index].id);
    },
    removeUrl(index) {
      this.urls.splice(index, 1);
      this.newFiles.splice(index, 1);
    },
    submitForm() {
      console.log("submitForm", this.body);

      let formData = new FormData();

      // Append files
      if (this.newFiles.length > 0) {
        this.newFiles.forEach((file) => {
          formData.append("images", file);
        });
      }

      // Append other data
      formData.append("body", this.body);
      formData.append(
        "attachmentsToRemove",
        JSON.stringify(this.attachmentsToRemove)
      );

      axios
        .post(`/api/posts/update/${this.post.id}/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("data", response.data);

          this.body = "";
          this.$refs.file.value = null;
          this.urls = [];
          window.location.reload();
        })
        .catch((error) => {
          console.error("error", error);
        });
    },
  },
};
</script>

<style>
.image-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.image-card {
  position: relative;
  width: 100px; /* 원하는 카드 너비 */
  margin-top: 10px;
}
.remove-button {
  position: absolute;
  top: -10px;
  right: -11px;
  font-size: 10px;
  font-weight: bold;
}
.remove-button img {
  width: 25px;
}
</style>

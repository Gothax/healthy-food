<template>
    <form v-on:submit.prevent="submitForm" method="post">
        <div class="p-4">
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Body"></textarea>
            <input v-model="category_id" type="text" placeholder="Category ID" class="p-4 w-full bg-gray-100 rounded-lg mt-2" />
            <input v-model="price" type="text" placeholder="Price" class="p-4 w-full bg-gray-100 rounded-lg mt-2" />
            <input v-model="name" type="text" placeholder="Product Name" class="p-4 w-full bg-gray-100 rounded-lg mt-2" />
            <input v-model="specific" type="text" placeholder="Specific" class="p-4 w-full bg-gray-100 rounded-lg mt-2" />

            <div id="preview" v-if="urls.length">
                <img v-for="(url, index) in urls" :key="index" :src="url" class="w-[100px] mt-3 rounded-xl" />
            </div>
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                <input type="file" ref="file" @change="onFileChange" multiple>
                Attach images
            </label>
            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
        </div>
    </form>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            body: '',
            category_id: '',
            price: '',
            name: '',
            specific: '',
            urls: [],
        }
    },

    methods: {
        onFileChange(e) {
            const files = e.target.files;
            this.urls = Array.from(files).map(file => URL.createObjectURL(file)); 
        },
        
        submitForm() {
            console.log('submitForm', this.body, this.category_id, this.price, this.name, this.specific)
            
            let formData = new FormData();
            Array.from(this.$refs.file.files).forEach(file => {
                formData.append('images', file);
            });
            formData.append('body', this.body);
            formData.append('category_id', this.category_id);
            formData.append('price', this.price);
            formData.append('name', this.name);
            formData.append('specific', this.specific);

            axios
                .post('/api/posts/create/product/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    this.body = ''
                    this.category_id = ''
                    this.price = ''
                    this.name = ''
                    this.specific = ''
                    this.$refs.file.value = null
                    this.urls = []
                    window.location.reload()

                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>
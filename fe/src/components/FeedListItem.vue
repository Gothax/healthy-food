<template>
    <div class="image-grid">
        <div class="content-type-label" v-if="post.content_type">
            {{ post.content_type }}
        </div>
        <template v-if="post.attachments.length">
            <img 
                :src="post.attachments[0].get_image" 
                class="image-item  mb-4 rounded-xl transition-transform duration-500 hover:scale-105"
                style="width: 500px; height: 300px; object-fit: cover;"
            
            >
        </template>
    </div>
</template>

<script>
export default {
    props: {
        post: Object
    },
}
</script>
<style scoped>
.image-grid {
    position: relative;
}

.content-type-label {
    position: absolute;
    top: 5px;
    left: 5px;
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 10px;
    z-index: 10;
}
</style>
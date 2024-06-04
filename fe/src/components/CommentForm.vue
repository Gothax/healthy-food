<!--CommentForm.vue  -->
<template>
    <!-- isCommentModalOpen = true로 넘어와서 모달창 열림  -->
    <div class="modal-wrap" v-show="isCommentModalOpen" @click="closeModal">
        <div class="modal-container" @click.stop="">
            <h2 class="text-lg font-bold mb-4">Comments</h2>
            <CommentItem v-for="comment in post.comments" :key="comment.id" :comment="comment" />
            <input v-model="newComment" placeholder="Add a comment" class="w-full p-2 border rounded" />
            <button @click="addComment" class="mt-2 p-2 bg-blue-500 text-white rounded">Comment</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import CommentItem from './CommentItem.vue'
// Post와 isCommentModalOpen을 Feeditem으로 보내줌 CommentForm이 자식
export default {
    props: {
        post: Object,
        isCommentModalOpen: Boolean
    },
    components: {
        CommentItem
    },
    data() {
        return {
            newComment: ''
        }
    },
    methods: {
        closeModal(event) {
            if (event.target.classList.contains('modal-wrap')) {
                this.$emit('closeModal');
            }
        },
        addComment() {
            axios.post(`/api/posts/${this.post.id}/comment/`, {
                body: this.newComment
            })
            .then(response => {
                this.post.comments.push(response.data);
                this.post.comments_count += 1;
                this.newComment = '';
            })
            .catch(error => {
                console.error('Error posting comment', error);
            });
        }
    }
}
</script>

<style scoped>
.modal-wrap {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4);
    z-index: 1000;
}
.modal-container {
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 550px;
    background: #fff;
    border-radius: 10px;
    padding: 20px;
    box-sizing: border-box;
    z-index: 1001;
}
</style>
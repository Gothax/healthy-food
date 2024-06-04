<template>
    <!-- isCommentModalOpen = true로 넘어와서 모달창 열림  -->
    <div class="modal-wrap" v-show="isCommentModalOpen" @click="closeModal">
        <!-- 내부 스크롤을 가진 모달 컨테이너 -->
        <div class="modal-container" @click.stop="">
            <h2 class="text-lg font-bold mb-4">Comments</h2>
            <!-- 댓글 컨테이너 -->
            <div class="comments-container">
                <CommentItem v-for="comment in post.comments" :key="comment.id" :comment="comment" />
            </div>
            <!-- 새로운 댓글 입력 폼 -->
            <input v-model="newComment" placeholder="Add a comment" class="w-full p-2 border rounded" />
            <button @click="addComment" class="mt-2 p-2 bg-blue-500 text-white rounded">Comment</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import CommentItem from './CommentItem.vue'

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
/* 외부 모달 창 */
.modal-wrap {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4);
    z-index: 1000;
}
/* 내부 모달 컨테이너 */
.modal-container {
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 550px;
    max-height: 80%; /* 모달 창의 최대 높이 설정 */
    background: #fff;
    border-radius: 10px;
    padding: 20px;
    box-sizing: border-box;
    z-index: 1001;
    display: flex;
    flex-direction: column;
    overflow-y: auto; /* 내부 스크롤 활성화 */
}
/* 댓글 컨테이너 */
.comments-container {
    flex-grow: 1;
    overflow-y: auto; /* 내부 스크롤 활성화 */
    max-height: calc(100vh - 250px); /* 최대 높이 설정 */
    margin-bottom: 10px; /* 댓글 영역 아래에 약간의 여백 추가 */
}
</style>

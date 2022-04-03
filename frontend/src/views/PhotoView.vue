<script setup>
import { onBeforeMount, getCurrentInstance, ref, inject } from "vue";
import { useRoute } from "vue-router";
import { getPhoto } from "../services/friendsApi";
import PhotoThumb from "../components/PhotoThumb.vue";
import StyledInput from "../components/StyledInput.vue";
import {
  sendComment,
  likeComment,
  likePhoto,
  deleteComment,
} from "../services/friendsApi";

const globals = getCurrentInstance().appContext.config.globalProperties;
const { user } = inject("user");

const route = useRoute();
const photoId = route.params.id;

const loadingComment = ref(false);
const photo = ref(null);
const comment = ref("");

onBeforeMount(async () => {
  try {
    const response = await getPhoto(photoId);
    photo.value = response.data.data;
  } catch (err) {
    globals.$emitter.emit("flag-message", {
      content: "Unable to retrieve photos.",
      modifier: "error",
    });

    photo.value = null;
  }
});

async function handlePhotoLike() {
  if (user.value) {
    const likes = new Set(photo.value.likes);
    const isUserInLikes = likes.has(user.value._id);

    try {
      if (isUserInLikes) {
        likes.delete(user.value._id);
      } else {
        likes.add(user.value._id);
      }

      photo.value.likes = Array.from(likes);
      await likePhoto(photoId);
    } catch (err) {
      if (isUserInLikes) {
        likes.add(user.value._id);
      } else {
        likes.delete(user.value._id);
      }

      photo.value.likes = Array.from(likes);
      globals.$emitter.emit("flag-message", {
        content: `Unable to ${isUserInLikes ? "dislike" : "like"} photo.`,
        modifier: "error",
      });
    }
  }
}

async function handleSendComment() {
  if (comment.value && user.value) {
    loadingComment.value = true;

    try {
      await sendComment(photoId, comment.value);
      const response = await getPhoto(photoId);
      photo.value = response.data.data;
      comment.value = "";
    } catch (err) {
      globals.$emitter.emit("flag-message", {
        content: "Unable to send the comment.",
        modifier: "error",
      });
    }

    loadingComment.value = false;
  }
}

async function handleDeleteComment(commentIndex) {
  if (user.value) {
    const comment = photo.value.comments[commentIndex];
    try {
      photo.value.comments.splice(commentIndex, 1);
      await deleteComment(comment._id);
    } catch (err) {
      photo.value.comments.splice(commentIndex, 0, comment);

      globals.$emitter.emit("flag-message", {
        content: `Unable to delete comment.`,
        modifier: "error",
      });
    }
  }
}

async function handleCommentLike(commentIndex) {
  if (user.value) {
    const comment = photo.value.comments[commentIndex];
    const likes = new Set(comment.likes);
    const isUserInLikes = likes.has(user.value._id);

    try {
      if (isUserInLikes) {
        likes.delete(user.value._id);
      } else {
        likes.add(user.value._id);
      }

      comment.likes = Array.from(likes);
      await likeComment(comment._id);
    } catch (err) {
      if (isUserInLikes) {
        likes.add(user.value._id);
      } else {
        likes.delete(user.value._id);
      }

      comment.likes = Array.from(likes);
      globals.$emitter.emit("flag-message", {
        content: `Unable to ${isUserInLikes ? "dislike" : "like"} comment.`,
        modifier: "error",
      });
    }
  }
}
</script>
<template>
  <div class="photo-view" v-if="photo">
    <PhotoThumb :url="photo.url" big class="photo-view__img" />
    <div class="community-interaction">
      <section class="photo-info">
        <span class="photo-title">{{ photo.title }}</span>
        <div class="photo-likes">
          <span>{{ photo.likes.length }}</span>
          <font-awesome-icon
            @click="handlePhotoLike"
            :class="{
              'photo-like__icon--liked': user && photo.likes.includes(user._id),
            }"
            class="photo-like__icon"
            icon="heart"
          />
        </div>
      </section>
      <section class="photo-comments">
        <StyledInput
          v-model="comment"
          :placeholder="user ? 'Write a comment' : 'Log in to interact'"
          :disabled="!user || loadingComment"
          @keypress.enter="handleSendComment"
        />
        <div class="comments-box">
          <div
            class="comment"
            v-for="(comment, index) in photo.comments"
            :key="index"
          >
            <div class="comment-header">
              <span class="comment-user">{{ comment.user.name }}</span>
              <div class="comment-actions">
                <span>{{ comment.likes.length }}</span>
                <font-awesome-icon
                  @click="() => handleCommentLike(index)"
                  :class="{
                    'comment-like__icon--liked':
                      user && comment.likes.includes(user._id),
                  }"
                  class="comment-like__icon"
                  icon="heart"
                />
                <font-awesome-icon
                  v-if="user && comment.user._id === user._id"
                  @click="() => handleDeleteComment(index)"
                  title="Delete photo"
                  class="comment-delete__icon"
                  icon="trash-can"
                />
              </div>
            </div>
            <span class="comment-label">{{ comment.content }}</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
<style scoped>
.photo-view {
  width: fit-content;
  max-width: 102.4rem;
  height: 50rem;
  display: flex;
  justify-content: center;
  margin: 1rem auto;
  background-color: var(--primary-color);
}

.photo-view__img {
  max-width: 76.4rem;
}

.community-interaction {
  width: 26rem;
  height: 50rem;
  background-color: var(--primary-color);
  display: flex;
  flex-direction: column;
}

.photo-info {
  display: flex;
  width: 100%;
  padding: 1rem;
  justify-content: space-between;
  align-items: center;
  height: 5rem;
}

.photo-likes {
  display: flex;
  align-items: center;
}

.photo-like__icon {
  margin-left: 0.6rem;
  font-size: 2.5rem;
}

.photo-comments {
  width: 100%;
  height: 45rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 1.6rem;
}

.comments-box {
  margin-top: 0.5rem;
  width: 100%;
  height: 100%;
  overflow-y: auto;
}

.comment {
  width: 22rem;
  display: flex;
  flex-direction: column;
  padding: 0.6rem;
  background-color: var(--secondary-color);
  margin: 1rem auto;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  border-bottom: 0.2rem solid var(--primary-color);
  font-size: 1.3rem;
  margin-bottom: 0.3rem;
  color: var(--primary-color);
}

.comment-actions {
  display: flex;
  justify-content: center;
  align-items: center;
}

.comment-like__icon,
.comment-delete__icon {
  margin-left: 0.2rem;
}

.photo-like__icon,
.comment-like__icon,
.comment-delete__icon {
  cursor: pointer;
}

.photo-like__icon--liked,
.comment-like__icon--liked,
.comment-delete__icon {
  color: var(--red-color);
}

@media screen and (max-width: 768px) {
  .photo-view {
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
  }

  .photo-view,
  .community-interaction {
    width: 100%;
  }
}
</style>

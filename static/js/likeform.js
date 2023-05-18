let formslike = document.querySelectorAll("[id^='likeform']");
let csrftokens = document.querySelector("[name=csrfmiddlewaretoken]").value;
formslike.forEach((likeform) => {
  likeform.addEventListener("submit", function (event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
    axios({
      method: "POST",
      url: `/${postId}/like/`,
      headers: { "X-CSRFToken": csrftoken },
    }).then((response) => {
      const likeBtn = document.querySelector(`#like-${postId}`);
      const isLikeUsers = response.data.is_like_users;
      const likeCount = response.data.like_count; // 좋아요 개수를 받아옴
      if (isLikeUsers === true) {
        likeBtn.innerHTML =
          '<i class="bi bi-heart-fill" style="color: red;"></i>';
      } else {
        likeBtn.innerHTML = '<i class="bi bi-heart" style="color: black;"></i>';
      }
      // 좋아요 개수 업데이트
      const likeCountElement = document.querySelector(`#like-count-${postId}`);
      // likeCountElement.textContent = likeCount;
      likeCountElement.textContent = `좋아요 ${likeCount}개`;
      // console.log(likeCount)
    });
  });
});

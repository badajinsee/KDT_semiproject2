const commentForms = document.querySelectorAll(".comments_create");
const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
console.log(commentForms);
commentForms.forEach((commentForm) => {
  const lis = commentForm.parentNode.getElementsByTagName("li");
  console.log(lis);
  Array.from(lis).forEach((li2, index) => {
    li2.querySelector("form").addEventListener("submit", function (event) {
      event.preventDefault();
      const commentId = event.target.dataset.commentId;
      const postId = event.target.dataset.postId;
      console.log("도달1");
      console.log(postId, commentId, index);
      axios
        .post(
          `/${postId}/comments/${commentId}/delete/`,
          {},
          {
            headers: { "X-CSRFToken": csrftoken },
          }
        )
        .then((response) => {
          console.log("도달2");
          li2.remove();
        });
    });
  });
  commentForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const csrftoken = document.querySelector(
      "[name = csrfmiddlewaretoken]"
    ).value;
    const parentcommentId = event.target.dataset.parentcommentId;
    const postId = event.target.dataset.postId;
    const li = document.createElement("li");
    const formData = new FormData(commentForm);
    const lis = commentForm.parentNode.getElementsByTagName("li");
    console.log(lis);

    axios
      .post(`/${postId}/comments/${parentcommentId}/`, formData, {
        headers: { "X-CSRFToken": csrftoken },
      })
      .then((response) => {
        const content = response.data.content;
        const postPk = response.data.postPk;
        const commentPk = response.data.commentPk;
        const postUser = response.data.postUser;

        const postUl = commentForm.parentNode.querySelector("ul");
        const commentLi = document.createElement("li");
        commentLi.innerHTML = `
          <div class="horizontal-container">
            <p class="bold">${User}</p> <p>&nbsp;&nbsp;&nbsp;</p> <p class="small-text">방금 전</p>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <p class="mb-2 mt-2">${content}</p>
            <form data-post-id="${postPk}" data-comment-id="${commentPk}" method="post">
              <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
              <input type="submit" class="btn btn-outline-primary" style="border:none; font-size:13px;" value="댓글삭제">
            </form>
          </div>
          <br>
        `;
        const inputText = commentForm.querySelector('form input[type="text"]');
        inputText.value = "";
        postUl.appendChild(commentLi);
        const scrollableDiv = document.querySelector(".scrollable-div");
        scrollableDiv.scrollTop = scrollableDiv.scrollHeight;
      });
  });
});

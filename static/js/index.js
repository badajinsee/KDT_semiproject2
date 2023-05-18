const commentForms = document.querySelectorAll("#comments_create");
// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
console.log(csrftoken)

commentForms.forEach((commentForm) => {
  const lis = commentForm.parentNode.getElementsByTagName("li");
  Array.from(lis).forEach((li, index) => {
    li.querySelector("form").addEventListener("submit", function (event) {
      
      console.log(csrftoken)

      event.preventDefault();
      const commentId = event.target.dataset.commentId;
      const postId = event.target.dataset.postId;
      axios
        .post(
          `/${postId}/comments/${commentId}/delete/`,
          {},
          {
            headers: { "X-CSRFToken": csrftoken },
          }
        )
        .then((response) => {
          li.remove();
        });
    });
  });

  commentForm.addEventListener("submit", function (event) {

console.log(csrftoken)
    event.preventDefault();
    const parentcommentId = event.target.dataset.parentcommentId;
    const postId = event.target.dataset.postId;
    const li = document.createElement("li");
    const formData = new FormData(commentForm);
    const lis = commentForm.parentNode.getElementsByTagName("li");

    axios
      .post(`/${postId}/comments/${parentcommentId}/`, formData, {
        headers: { "X-CSRFToken": csrftoken },
      })
      .then((response) => {
        const content = response.data.content;
        const postPk = response.data.postPk;
        const commentPk = response.data.commentPk;
        const User = response.data.User;

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
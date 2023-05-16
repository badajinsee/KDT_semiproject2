// 부모가 있으면 검색해서 내부에
// 부모가 없으면 바로 아래에
const commentForm = document.querySelector('#comments_create');
const cocommentForm = document.querySelector('#cocomments_create')
// h1.innerText = "asd;lfkajsd;lfkj;sadlkf"
console.log("후아아아ㅏㅇ아ㅏ")
commentForm.addEventListener('submit', function (event) {
  console.log("후아아아ㅏㅇ아ㅏ2")
  event.preventDefault()
  const csrftoken = document.querySelector('[name = csrfmiddlewaretoken]').value
  const parentcommentId = event.target.dataset.parentcommentId
  const postId = event.target.dataset.postId

  // create li element
  const li = document.createElement('li');

  // create p element
  const p = document.createElement('p');

  // create comments_delete form
  const commentsDeleteForm = document.createElement('form');
  commentsDeleteForm.setAttribute('id', 'comments_delete');
  commentsDeleteForm.setAttribute('method', 'post');


  const csrfTokenInput = document.createElement('input');
  csrfTokenInput.setAttribute('type', 'hidden');
  csrfTokenInput.setAttribute('name', 'csrfmiddlewaretoken');
  csrfTokenInput.setAttribute('value', `${csrftoken}`);
  commentsDeleteForm.appendChild(csrfTokenInput);

  const commentsDeleteSubmit = document.createElement('input');
  commentsDeleteSubmit.setAttribute('type', 'submit');
  commentsDeleteSubmit.setAttribute('value', '댓글삭제');
  commentsDeleteForm.appendChild(commentsDeleteSubmit);

  // create cocomments_create form
  const cocommentsCreateForm = document.createElement('form');
  cocommentsCreateForm.setAttribute('id', 'cocomments_create');
  cocommentsCreateForm.setAttribute('data-post-id', postId);
  cocommentsCreateForm.setAttribute('method', 'post');

  const cocommentsCreateCsrfTokenInput = document.createElement('input');
  cocommentsCreateCsrfTokenInput.setAttribute('type', 'hidden');
  cocommentsCreateCsrfTokenInput.setAttribute('name', 'csrfmiddlewaretoken');
  cocommentsCreateCsrfTokenInput.setAttribute('value', `${csrftoken}`);
  cocommentsCreateForm.appendChild(cocommentsCreateCsrfTokenInput);

  const commentLabel = document.createElement('label');
  commentLabel.innerHTML = 'Content: ';
  cocommentsCreateForm.appendChild(commentLabel);

  const commentTextInput = document.createElement('input');
  commentTextInput.setAttribute('type', 'text');
  commentTextInput.setAttribute('name', 'content');
  cocommentsCreateForm.appendChild(commentTextInput);

  const cocommentsCreateSubmit = document.createElement('input');
  cocommentsCreateSubmit.setAttribute('type', 'submit');
  cocommentsCreateSubmit.setAttribute('value', '대댓글 등록');
  cocommentsCreateForm.appendChild(cocommentsCreateSubmit);

  // append all elements to li element



  // li.appendChild(form);
  const formData = new FormData(commentForm);
  console.log("후아아아아아아ㅏ")
  axios.post(`/${postId}/comments/${parentcommentId}/`, formData, {
    headers: { 'X-CSRFToken': csrftoken }
  })
    .then((response) => {
      const content = response.data.content
      const commentPk = response.data.comment_pk

      p.textContent = `댓글 : ${content}`;
      commentsDeleteForm.setAttribute('action', `${postId}/comments/${commentPk}/delete`);
      cocommentsCreateForm.setAttribute('data-parentcomment-id', commentPk);
      cocommentsCreateForm.setAttribute('action', `/${postId}/comments/${commentPk}/delete/`);

      li.appendChild(p);
      li.appendChild(commentsDeleteForm);
      li.appendChild(cocommentsCreateForm);

      const postUl = document.querySelector(`#comment${commentPk}`)
      postUl.appendChild(li)


    })
})

// li p 댓글 :
// cocommentForm.addEventListener('submit', function (event) {
//   event.preventDefault()
//   const csrftoken = document.querySelector('[name = csrfmiddlewaretoken]').value
//   const parentcommentId = event.target.dataset.parentcommentId
//   const postId = event.target.dataset.postId

//   const commentli = document.querySelector('#comment > li');
//   const coli = commentli.cloneNode(true)
//   const cocommentli = document.querySelector(`#comment${parentcommentId} > li`)
//   const cocoli = cocommentli.cloneNode(true)

//   // li.appendChild(form);
//   const formData = new FormData(commentForm);
//   axios.post(`/${postId}/comments/${parentcommentId}/`, formData, {
//     headers: { 'X-CSRFToken': csrftoken }
//   })
//     .then((response) => {
//       const content = response.data.content
//       const commentPk = response.data.comment_pk
//       const postPk = response.data.post_pk

//       if (parentcommentId != '0') {
//         cocoli.querySelector('form').setAttribute('action', `/${postPk}/comments/${commentPk}/delete/`);
//         cocoli.querySelector('p').innerText = content;
//         const postUl = document.querySelector(`#comment #comment${parentcommentId}`) // id가 comment인 ul을 찾아서 그 안에 id가 parentcommentId를 찾아서 li를 삽입
//         postUl.appendChild(cocoli)
//       } else {
//         coli.querySelector('form').setAttribute('action', `/${postId}/comments/${commentPk}/delete/`);
//         coli.querySelector('p').innerText = content;
//         const postUl = document.querySelector('#comment')
//         postUl.appendChild(coli)
//       }


//     })
// })
function deleteStudent(id) {
  fetch("/delete-student", {
    method: "POST",
    body: JSON.stringify({id: id}),
  }).then((_res) => {
    window.location.href = "/";
  });
}

const imageInput = document.getElementById("image_to_upload");
imageInput.addEventListener("change", () => {
  const currentFile = imageInput.files;
  if (currentFile.length > 0) {
    for (const file of currentFile) {
      if (file.type.match(/image.*/i)) {
        let reader = new FileReader();
        reader.addEventListener("load", () => {
          const form = document.getElementById("hidden_form");
          const input = document.createElement("input");
          input.setAttribute("name", "image_base_64");
          input.setAttribute("value", reader.result);
          form.append(input);
          form.submit();
        });
        reader.readAsDataURL(file);
      }
    }
  }
});

const btn = document.querySelectorAll(".btn");
const flag = document.querySelectorAll("span");
const content = document.querySelectorAll(".content");

for (let i = 0; i < btn.length; i++) {
  btn[i].addEventListener("click", () => {
    flag[i].classList.toggle("off");
  });
  if (flag[i].classList.contains("off") == true) {
    console.log("off");
    content[i].classList.add("notContent");
  }
}

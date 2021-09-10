const repeatBtn = document.querySelectorAll(".repeatBtn");
const btn = document.querySelectorAll(".btn");
// const check = document.querySelectorAll(".repeatBtnrepeatBtn span");
for (let i = 0; i < btn.length; i++) {
  //   console.log(repeatBtn[i]);
  btn[i].addEventListener("click", () => {
    // console.log(btn[i]);
    repeatBtn[i].classList.toggle("activ");
  });
}

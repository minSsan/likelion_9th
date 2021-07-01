
document.querySelector(".kw").addEventListener('change', function() {
    document.querySelector('#kw').value = this.value;
    document.querySelector('#searchForm').submit();
});

document.querySelector(".op").addEventListener("click", function() {
    document.querySelector('#op').value = this.value;
    document.querySelector('#searchForm').submit();
})

document.querySelector(".op2").addEventListener("click", function() {
    document.querySelector('#op').value = this.value;
    document.querySelector('#kw').value = this.value;
    document.querySelector('#searchForm').submit();
})
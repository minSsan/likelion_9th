document.getElementById('if').setAttribute('class', 'nav-link active')

document.querySelector(".kw").addEventListener('change', function() {
    document.querySelector('#kw').value = this.value;
    document.querySelector('#page').value = '1';
    document.querySelector('#searchForm').submit();
});

document.querySelector(".op").addEventListener("click", function() {
    document.querySelector('#op').value = this.value;
    document.querySelector('#page').value = '1';
    document.querySelector('#searchForm').submit();
})

document.querySelector(".op2").addEventListener("click", function() {
    document.querySelector('#op').value = this.value;
    document.querySelector('#kw').value = this.value;
    document.querySelector('#page').value = '1';
    document.querySelector('#searchForm').submit();
})

document.querySelectorAll('.page-link').forEach(function(ele) {
    ele.addEventListener("click", function() {
        document.querySelector('#page').value = this.dataset.page;
        document.querySelector('#searchForm').submit();
    })
})

document.querySelector('.child').addEventListener('click', function() {
    document.querySelector('.adult').style.display= "block";
    this.style.display="none";
})

document.querySelector('.adult').addEventListener('click', function() {
    document.querySelector('.child').style.display= "block";
    this.style.display="none";
})
var lis=document.querySelector('ul').querySelectorAll('li');
var divs=document.querySelector('.neirong').querySelectorAll('div');
for(var i=0;i<lis.length;i++){
    lis[i].setAttribute('index',i);
    lis[i].onclick=function(){
        for(var i=0;i<lis.length;i++){
            lis[i].className='';
        }
        this.className='choose';
        var index=this.getAttribute('index');
        for(var i=0;i<divs.length;i++){
            divs[i].style.display='none';
        }
        divs[index].style.display='block';
    }
}

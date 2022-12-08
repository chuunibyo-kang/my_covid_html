// 生成实时时间的函数
function get_real_time(){
    var date = new Date();
    //获取年份
    var year = date.getFullYear();  
    //获取月份(月份有点特殊，需要手动+1才能正常显示)
    var month = date.getMonth()+1;   
     //获取日
    var day= date.getDate(); 
     //获取小时  
    var hour = date.getHours();  
    //获取分钟     
    var minute = date.getMinutes();  
    //获取秒
    var second = date.getSeconds();  
    // 给小于0的月、日、时、分、秒，在字符串前加“0”
    month=check_time(month);
    day=check_time(day);
    minute=check_time(minute);   
    hour = check_time(hour);
    second =check_time(second);    
    //将年、月、日、时、分、秒赋值给date参数
    date = year+"-"+month+"-"+day+" "+hour+":"+minute+":"+second;  
    // 将返回值传到这个id为real_time的HTML标签中
    document.getElementById("real_time").innerHTML=date;
  }       
   // 检查返回的数值是否是小于0，如果是就加0
   function check_time(i)   {   
  if (i<10){
      i="0" + i;
  }   
     return i;
  }          
  //先调用获取时间的方法     
  get_real_time();  
  //这一句能实现间隔1000毫秒执行一次get_real_time方法，是实现实时显示的核心语句
  setInterval("get_real_time()",1000);
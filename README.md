# cloudtools
##aws.tool.belt OR aws.swissarmy.knife

sharing the tools and scripts i use to make my AWS quality of life.
the focus is on making the day-to-day work smoother

this is work in progress, will add them tools one at a time.



##1 ec2ls (the `ls` for ec2 instances)
bash/cli listing of the AWS ec2 instances
  allows to filter by env (assuming there is an 'Env' tag on the instance, or by name: prefix/suffix)
  provides the list of nodes, sorted by creation time
  
  it also creates the standard ssh -i ~/.ssh/abc.pem ubuntu@IP_address command line and puts it in the clipboard
  so all is left is to paste it.
  
  when the result includes multiple instances, the last is pasted by default or the index (-i flag) can be used to 
  select which one to use.
   -1 is the last, -2 the one before last, 1 is the first etc.
   
   
   
   
  
  
  
  
 

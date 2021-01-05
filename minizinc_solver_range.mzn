int: num;
int: cap;
int: refill;
array [1..num] of int: fun;
int: goal;

array [1..num] of var 1..cap: token;
array [1..num] of var 1..cap: play;
var -100..1000: total_fun;

constraint total_fun = sum(i in 1..num)(play[i]*fun[i]);
constraint total_fun >= goal;
constraint ((token[1]=cap)/\
            forall(i in 2..num)
            (exists(x in 0..(cap+refill))
             ((x = token[i-1]-play[i-1]+refill)/\
              (x>cap -> token[i]=cap)/\
              (x<=cap -> token[i]=x))));
           
constraint forall(i in 1..num)(play[i]>=1 /\ play[i]<=token[i]);

solve maximize total_fun;
output ["max total fun = \(total_fun)\n"];

int: num;
int: cap;
int: refill;
array [1..num] of int: fun;
int: goal;

array [1..num] of var int: token;
array [1..num] of var int: play;

constraint sum(i in 1..num)(play[i]*fun[i]) >= goal;
constraint ((token[1]=cap)/\
            forall(i in 2..num)
            (exists(x in 0..(cap+refill))
             ((x = token[i-1]-play[i-1]+refill)/\
              (x>cap -> token[i]=cap)/\
              (x<=cap -> token[i]=x))));
           
constraint forall(i in 1..num)((if fun[i]<0 then play[i]=1 else play[i]>=1 endif) /\ play[i]<=token[i]);

solve maximize sum(i in 1..num)(play[i]*fun[i]);
output ["max total fun = \(sum(i in 1..num)(play[i]*fun[i]))\n"];

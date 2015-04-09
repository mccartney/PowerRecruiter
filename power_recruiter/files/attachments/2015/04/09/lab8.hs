-- lab 8
import qualified Data.Map as M (empty, insert, lookup, Map, assocs, toAscList)
import Control.Monad.Reader
import Control.Monad.State
import Data.Maybe

-- assocs :: Map k a -> [(k, a)]

type Var = String

data Exp = EInt Int | EOp  Op Exp Exp | EVar Var | ELet Var Exp Exp  -- let var = e1 in e2

data Op = OpAdd | OpMul | OpSub

type MyEnv = M.Map Var Int

fop :: Op -> Int -> Int -> Int
fop OpAdd = (+)
fop OpMul = (*)
fop OpSub = (-)

eval :: Exp -> Reader MyEnv Int
eval (EInt k) = return k
eval (EOp op exp1 exp2) = do
	e1 <- eval exp1
	e2 <- eval exp2
	return $ (fop op) e1 e2
-- eval1 (EOp op e1 e2) = liftM2 (fop op) (eval e1) (eval e2)
eval (EVar var) = do
	map <- ask 
	return $ fromMaybe (error ("undefined variable: " ++ var)) $ M.lookup var map  

eval (ELet var exp1 exp2) = do
	e1 <- eval exp1
	local (M.insert var e1) (eval exp2)


evalExp :: Exp -> Int
evalExp e = runReader (eval e) M.empty -- runReader odpala readera, ktorym jest eval e, a srodowisko dla readera to --jest pust ampa


evalExpMap :: Exp -> MyState -> Int
evalExpMap e m = runReader (eval e) m

test = ELet "x" (ELet "y" (EOp OpAdd (EInt 6) (EInt 9))
                      (EOp OpSub y (EInt 1)))
                (EOp OpMul x (EInt 3))
    where x = EVar "x"
          y = EVar "y"


-- TREE
data Tree a = Empty | Node (Tree a) a (Tree a) deriving (Eq, Ord, Show)
--ren :: Tree a -> Reader Int (Tree Int)
--ren :: Tree a -> (Int -> Tree Int) bo -> r jest monada reader
ren Empty = return Empty
ren (Node l _ p) = do
	k <- ask
	nl <- local (+1) (ren l)
	np <- local (+1) (ren p)
	return $ Node nl k np

renumber1 d = ren d 0


-- lab9
-- a. renumber z uzyciem State

-- b.  Rozszerzmy język z poprzedniego zadania o instrukcje języka Tiny (patrz przedmiot Semantyka i Weryfikacja Pro-- gramów)

-- Stmt:   S ::= skip | x := e | S1;S2 | if b then S1 else S2 | while b do S

data Stmt = SSkip | SAssign Var Exp | SComp Stmt Stmt | SIf Exp Stmt Stmt | SWhile Exp Stmt   

--glowna    
--execStmt :: Stmt -> IO ()
-- execStmt s = wypisz $ execState (exec s) M.empty 

--wypisz :: MyState -> IO ()


-- execState da nam mape 
-- a potem tu printujemy te mape cala .. print .. evalState

-- kiedy newtype? -> data z 1 konstruktorem 
type MyState = M.Map Var Int 

-- State stan wynik (tutaj wynik to unit, bo nic te funckje nie zwracaja, tylko zmieniaja stan)
exec :: Stmt -> State MyState () -- () to brak wyniku

exec (SAssign var exp) = do 
	 map <- get -- pobiera stan
	 put $ M.insert var (evalExpMap exp map) map
	 --return () -- moge to dodac?

exec SSkip = return ()

exec (SComp stmt1 stmt2) = do
     exec stmt1
     exec stmt2

exec (SIf exp stmt1 stmt2) = do
     map <- get
     if (evalExpMap exp map > 0) 
     	then exec stmt1
     	else exec stmt2

exec (SWhile exp stmt) = do
     map <- get     
     if (evalExpMap exp map > 0)
     	then exec $ SComp stmt (SWhile exp stmt)
	else return ()  

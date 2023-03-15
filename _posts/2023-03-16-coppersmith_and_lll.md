--- 
layout: post
title:  "Coppersmith & LLL algorithm 筆記"
date: 2023-03-16
tags:
 - crypto

categories: notes
---
# Coppersmith's method 及 LLL algorithm

上學期修了計安，打了一堆CTF的同時，也認識到了Coppersmith以及LLL這系列的密碼學魔法，但是由於我理解力不足，所以花了很久的時間才稍微了解一點，因此寫這篇文來紀錄一下免得又忘記XD。
<!--description-->
## Introduction

在做一些題目的時候很常遇到要解類似下面的方程式：
$$
F(x)=x^n+a_{n-1}x^{n-1}+...+a_1x+a_0  \\
\text{solve } F(x_0)\equiv0 \text{  (mod N) with }x_0<X
$$
若是改在 $\Z$ 上面要解這種多項式，方法很多，如 [Newton's Method](https://zh.wikipedia.org/wiki/%E7%89%9B%E9%A1%BF%E6%B3%95)。但我們是在 $\Z_N$，於是要想辦法轉移到 $\Z$ 去做這個問題。 也就是，我們想讓問題從 $F(x)=0 \mod{M}, x<X$ 變成 $g(x)=0, x\in\Z$ 。

### LLL algorithm

LLL 演算法，全名 Lenstra–Lenstra–Lovász Algorithm。本文不會說明他的內部實際運算過程。

LLL 是用來計算 Shortest Vector Problem 的演算法，SVP 是 NP-Hard，所以它只會Approximate，但是可以在多項式時間內做完。基本概念是：給定幾個向量作為基底，在他們湊出來的離散 Lattice 中，試圖找出最短的向量。

LLL 找到的向量 $\vec{v}$，Best case： 
$$
||v|| \le 2^{(n-1)/4}|\det{L}|^{(1/n)}
$$
 Average case:
$$
||v|| \le 1.02^n|\det{L}|^{(1/n)}
$$


### Howgrave-Graham Theorem

這裡要介紹一個定理，形式如下：

令 $g(x)$ 為一個單變數 $d$ 次多項式，$m\in\N$， 則若滿足
$$
g(x_0)=0 \mod{N^m} \ \text{ where }x_0 \le X  \\
||g(xX)||<\frac{N^m}{\sqrt d}
$$
則
$$
g(x_0)=0
$$
在 $\Z$ 上也滿足。此處的 $||g(xX)||$ 指將 $g(xX)$ 展開後的係數當成一個向量算絕對值。

換句話說，這個定理的意義其實很簡單：*只要 $g(x)$ 的係數向量長和 $x_0$ 的 Upper bound 夠小，就能直接把它當成在 $\Z$ 上解。* 

因此，我們的目標便是找到一個函數 $g(x)$ ，使得當$x_0$滿足$f(x)=0 \mod N$ ，會有 $g(x_0)\in N^m\Z$，同時係數又要小。

那麼我們要怎麼找到這個函數？

> 這個定理可以用柯西不等式證明，此處略過，若有需要請參考 Reference 的書。

## Constructing the matrix

顯然 $f(x)$ 本身會符合條件，連帶的 $xf(x), x^2f(x)...$ 以及他們的常數倍也會符合。

也容易看出 $g(x)\in N^m\Z+N^mx\Z+N^mx^2\Z+...$ 都會符合條件。把這個跟前面的$f(x)$加起來也明顯可以拿來用。

換句話說，若把 $\{N^m, N^mx, N^mx^2..., f(x),xf(x),...\}$ 用來當作basis，線性組合湊出來的整個空間便可當作我們 $g(x)$ 的候選對象。

由於前面 Howgrave-Graham 有 $||g(xX)||$ $<\frac{N^m}{\sqrt d}$ 這個限制，希望 $d$ 盡可能小，因此大於 $f(x)$ degree 的項，如 $N^mx^{n+1}$ 等可以不用，下個步驟會比較好做。

接下來，我們必須想辦法利用 LLL 使 $$||g(xX)||$$ 盡可能變小。隨便舉例，若要解 $(a+x_0)^2=c$可以這樣列：
$$
B=\{N,Nx,f(x)\} \\
f(x_0)=(a+x_0)^2-c=0 \\
x_0 \le X
$$
來建立矩陣，會變成：
$$
B=\begin{bmatrix}
X^2 & 2aX & a^2-c  \\
& NX \\
& & N
\end{bmatrix}
$$
用 LLL 下去之後得到的向量，如果滿足 H-G Theorem 條件，把它當成多項式係數就可以用一般方法直接解了。(sage 可以用 `small_roots`)

> 如果想要的話，也可以乘起來做出 $x^2f(x)^2$之類的東西拿來當作基底，其他根據題目的不同也可以自己湊，重點是湊出的多項式要可以作到$g(x_0)=0$就好。ex. 如果現在 mod $p$，可以拿RSA的$N=pq$ 當作一個基底。發揮創意就對了。



## When can Coppersmith's method be used?

這裡介紹另一個定理。

### Coppersmith's theorem

給定 $d$ 次多項式 $f(x)$，可以快速找到 $f(r)=0 \mod N$ 的所有 $|r| < N^{1/d}$ 的解。(就是用我們上面的方法)。

這個定理基本上就是 LLL 的輸出向量長度上界 $||v|| \le 1.02^n|\det{L}|^{(1/n)}$，加上 H-G 的 $||g(xX)||<\frac{N}{\sqrt d}$ 而已。

因此要判斷湊出來的矩陣能不能用，可以大概用
$$
|\det L|^{1/d} < N
$$
來算 $X$ 必須要多小才會夠。

> 有可能湊出來的矩陣會讓$X$的上限太小，這時候可以如前面說的發揮創意亂湊 basis，把矩陣次數弄大，有可能會讓上限突然變小也說不定 XD
>
> 另外，LLL 不一定要用在 Coppersmith 裡頭，有可能算出 $\vec{u}B=\vec{v}$，然後用 $u, v$ 裡頭透露出的某些東西就解掉了。

## Conclusion

Coppersmith's method 就是想辦法用一些手段，把一個在modular ring上面的求根問題，挪到整數上來做。這些手段包括利用 Howgrave-Graham 定理，以及用 LLL 做出符合條件的多項式，然後便能簡單求解。

## References

* [Coppersmith / Howgrave-Graham and LLL, Tanja Lange, Eindhoven University of Technology.](http://hyperelliptic.org/tanja/teaching/crypto20/20200922-lll.pdf)

* [Chapter 19, Mathematics of Public Key Cryptography, Steven Galbraith.](https://www.math.auckland.ac.nz/~sgal018/crypto-book/ch19.pdf)

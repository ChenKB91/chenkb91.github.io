---
layout: post
title:  "How to reverse engineer a flash program (.swf) after 2020"
date:   2022-06-18
tags:
  - Reverse
  - Flash
categories: notes
---

Adobe在2020年底時宣布停止支援flash，並將所有flash的資源都從官網上撤掉。但有時在各種情況之下，我們還是可能需要reverse一些flash程式，那這時我們該怎麼辦呢？ 本篇文章將會簡單解釋流程。
<!--description-->
# 步驟
## Decompile
反編譯程式這裡推薦用[FFDec](https://github.com/jindrapetrik/jpexs-decompiler)，這是我在搜尋之下查到唯一的近幾年還有在維護的程式。

在安裝之後，用FFDec開啟你的.swf，理論上在畫面的中間可以看到FFDec會將其decompile成ActionScript，基本上就可以當作pseudocode看了。

若你想要patch這個程式，在右邊可以看到更底層一點的P-code，按底下的編輯功能可以直接修改，只是改一些變數的話這樣就很夠用了。在修改完成之後，左上角可以直接把patch後的程式儲存到新的檔案，可供執行。

## Execution
很不幸的，Adobe在2020年後看來是把官網上所有可以用來執行flash程式的東西全部趕盡殺絕了。不過，我們還有一個方法可以拿到以前的舊檔案，那就是使用Internet Archive，在此我們可以拿到相當方便的 [Adobe flash Player debug projector](https://archive.org/details/flashplayer_32_sa_debug_2)。

在開啟程式之後，左上角 File > Open 可以打開我們patch過的.swf，若一切運作正常，我們就能成功執行這些被我們動過手腳的flash了。
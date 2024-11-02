以下是一篇新聞，請根據 `title` 和 `summary` 的內容，分析每篇文章是否與"__theme__"直接相關。

衡量相關性的標準：
1. 關鍵字匹配：檢查 `title` 和 `summary` 是否包含與主題相關的關鍵字或同義詞，例如「人工智慧」、「AI」、「醫療」。
2. 語意相關性：若 `summary` 顯示文章探討主題範疇，如人工智慧在診斷或治療的應用，則視為相關。
3. 文章重點：若 `title` 明確指向主題範疇則視為相關。若重點偏離主題（如描述醫療設備但無AI內容），則視為不相關。

文章：
__news_article_summary__

主題描述：__theme_description__

回答方式：以JSON格式返回True或False，Respond only using json format
使用以下格式：
```json
{
"is_related": bool
}
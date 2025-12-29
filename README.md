# classes_table

# 选课逻辑
- prefer 为true的 (prefer, category) 为key 索引各条 class schedule 1
- prefer 为false的 (priority, category) 为key 索引各条 class schedule 2
- 先以 day sort {class schedule 1 dict} 然后 以day / priority sort {class schedule 2 dict}
- 遍历两个dict，然后加两个dict 判断，day dict 和 category dict 以限制 day 和 category
- 每轮 确认 
    - 那天的 课有没有超过 2节，如果超过，后面的class skip
    - 累计的 category的，有没有超过 1节，如果超过，后面的 clss skip

# 需要加的内容
[x] 课程显示 需要加 排序，比如按照日期 时间排序 --- 在data_deal 里有 --- 也加到了data 里
[] 需要考虑生理期如何排课
[] 之后需要呈现的，排好的 课 + block time
[] 看如何用交互式界面，运行前期的data 输入

## 可能需要补充的逻辑
- 按照 上课地点？但是这个还没想好
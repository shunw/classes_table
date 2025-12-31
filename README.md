# classes_table

# 选课逻辑
- prefer 为true的 (prefer, category) 为key 索引各条 class schedule 1
- prefer 为false的 (priority, category) 为key 索引各条 class schedule 2
- 先以 day sort {class schedule 1 dict} 然后 以day / priority sort {class schedule 2 dict}
- 遍历两个dict，然后加两个dict 判断，day dict 和 category dict 以限制 day 和 category
- 每轮 确认 
    - 那天的 课有没有超过 2节，如果超过，后面的class skip
    - 累计的 category的，有没有超过 1节，如果超过，后面的 clss skip


# 问答式逻辑 --- 为了输入课程信息
目的是为了要把输入的信息放入到对应的csv文件中去，主要输入的 csv文件为 class_schedule

## 主信息输入 class schedule的输入
### 自动生成的：
- id 可以自动生成，往后顺延，id必须唯一

### 可以自由输入，但是有格式需求：
- start_time 可以自由输入，但是需要限定格式
- day， 1-7

### 有id 限定，需按照id 输入
- class_id 为输入，但是需要提示哪个课是 哪个id，如果没有对应的 id，需要进入另外一个 先输入课程信息的 process，然后再跳出来，继续这个信息输入
- loc_id 为输入，但是需要提示哪个loc 是哪个id，同理，没有对应的id 需进入另外一个 程序

### bool型
- preferred

## 步骤：
- feat：input 信息可以 进入到对应的 csv [done]
- feat：terminal show 对应的信息和 id [done]
- feat：确认是否会有duplicate，如果有duplicate 应该如何操作？（所有录入 csv文件的 terminal的 输入都需要确认是否有 duplicate）[done]
- feat：如果没有对应的 课程id 应该如何操作，process [done]
- feat：如果想删除对应的条目，应该如何操作？
- feat: 如果想 中途终止，或者取消应该 如何操作？/ 增设一直 输入的 process，除非有 按特殊按键，然后终止，需要在界面上有对应的提示 [done]
- bug：为啥有时 writer row会写到上面一行的csv里去

# 需要加的内容
[x] 课程显示 需要加 排序，比如按照日期 时间排序 --- 在data_deal 里有 --- 也加到了data 里
[] 需要考虑生理期如何排课
[] 之后需要呈现的，排好的 课 + block time
[] 看如何用交互式界面，运行前期的data 输入

## 可能需要补充的逻辑
- 按照 上课地点？但是这个还没想好
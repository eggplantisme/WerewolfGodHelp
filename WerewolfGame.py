from unittest import result


class Game:
    sentence = ["天黑请闭眼。",
                "狼人请睁眼，狼人请确认队友身份...",
                "狼人请选择击杀目标，狼人请统一意见，狼人请闭眼。",
                "预言家请睁眼...",
                "预言家今晚查验谁的身份，好人是这个，坏人是这个，他是这个。预言家请闭眼。",
                "女巫请睁眼...",
                "今晚这个玩家死了, 你有一瓶解药你要救么，你有一瓶毒药你要毒么，你选择毒谁。女巫请闭眼。",
                "守卫请睁眼...",
                "今晚你想守护的目标是。守卫请闭眼。"
                "猎人请睁眼...",
                "今晚你的开枪状态是这个，你要带走谁。猎人请闭眼。",
                "白痴请睁眼...",
                "白痴请闭眼...",
                "天亮了"]

    def __init__(self):
        self.playerNames = ["请选择", "白狼王", "黑狼王", "恶灵骑士", "预言家", "女巫", "守卫", "猎人", "白痴"]
        self.n = 8  # 诸神黄昏8人场
        self.player = [None] * (self.n + 1)
        self.isKillSide = False  # 是否屠边，这里没啥用
        self.dayNum = 1  # 游戏天数
        # bad guy
        self.wolf = []  # [{'id': int, 'isLive': True/False}]
        self.blackWolfKing = dict({'id': 0, 'name': '黑狼王', 'isLive': True, 'canKill': False})
        self.whiteWolfKing = dict({'id': 0, 'name': '白狼王', 'isLive': True})
        self.evilKnight = dict({'id': 0, 'name': '恶灵骑士', 'isLive': True})
        # good guy
        self.predictor = dict({'id': 0, 'name': '预言家', 'isLive': True})
        self.witch = dict({'id': 0, 'name': '女巫', 'isLive': True, 'save': 1, 'poison': 1})
        self.hunter = dict({'id': 0, 'name': '猎人', 'isLive': True, 'canShot': False})
        self.idiot = dict({'id': 0, 'name': '白痴', 'isLive': True})
        self.guard = dict({'id': 0, 'name': '守卫', 'isLive': True, 'lastGuardId': 0})
        self.people = []
        # action
        self.save = []  # True/False
        self.poison = []
        self.kill = []
        self.shot = []
        self.look = []
        self.protect = []
        self.blackKill = []
        self.whiteKill = []
        self.evilKill = []
        self.vote = []

    def isEnd(self):
        """
        return 1 好人胜利
        -1 狼人胜利
        0 没有结束
        """
        # TODO 其他情况，简化游戏程序
        if self.predictor['isLive'] is False and self.witch['isLive'] is False and self.hunter['isLive'] is False and self.idiot['isLive'] is False and self.guard['isLive'] is False:
            return -1
        if self.blackWolfKing['isLive'] is False and self.whiteWolfKing['isLive'] is False and self.evilKnight['isLive'] is False:
            return 1
        return 0

    def summaryOneNight(self):
        # 流程
        flow = "*******记录*******\n"
        if self.kill[-1] != 0:
            flow += "*今晚狼刀了" + str(self.player[self.kill[-1]]['id']) + "号(" + self.player[self.kill[-1]]['name'] + ')\n'
        if self.look[-1] != 0:
            flow += "*今晚预言家查验了" + str(self.player[self.look[-1]]['id']) + "号(" + self.player[self.look[-1]]['name'] + ')\n'

        if self.save[-1] is True:
            flow += "*今晚女巫" + "使用了" + "解药\n"
            self.witch['save'] = 0
        else:
            flow += "*今晚女巫" + "没使用" + "解药\n"
        if self.poison[-1] == 0:
            flow += "*今晚女巫" + "没使用" + "毒药\n"
        else:
            flow += "*今晚女巫毒了" + str(self.player[self.poison[-1]]['id']) + "号(" + self.player[self.poison[-1]]['name'] + ')\n'
            self.witch['poison'] = 0
        
        if self.protect[-1] != 0:
            flow += "*今晚守卫守护了" + str(self.player[self.protect[-1]]['id']) + "号(" + self.player[self.protect[-1]]['name'] + ')\n'

        if self.hunter['canShot'] is True:
            flow += "*今晚猎人可以开枪,"
            if self.shot[-1] == 0:
                flow += "但猎人选择不开枪\n"
            else:
                flow += "猎人开枪带走了" + str(self.player[self.shot[-1]]['id']) + "号(" + self.player[self.shot[-1]]['name'] + ')\n'
        else:
            flow += "*今晚猎人不能开枪\n"
        
        if self.blackWolfKing['canKill'] is True:
            flow += "*今晚黑狼王可以发动技能,"
            if self.blackKill[-1] == 0:
                flow += "但黑狼王选择不带人\n"
            else:
                flow += "黑狼王带走了" + str(self.player[self.blackKill[-1]]['id']) + "号(" + self.player[self.blackKill[-1]]['name'] + ')\n'
        else:
            flow += "*今晚黑狼王不能发动技能\n"
        flow += "******记录结束******\n"
        # 死亡的人
        dead_id = []
        if self.shot[-1] is not 0:
            dead_id.append(self.shot[-1])
        if self.save[-1] is not True and self.protect[-1] != self.kill[-1]:
            dead_id.append(self.kill[-1])
        if self.blackKill[-1] is not 0:
            dead_id.append(self.blackKill[-1])
        if self.look[-1] == self.evilKnight['id']:
            dead_id.append(self.predictor['id'])
        if self.poison[-1] is not 0:
            if self.poison[-1] == self.evilKnight['id'] and self.look[-1] == self.evilKnight['id']:
                pass
            elif self.poison[-1] == self.evilKnight['id'] and self.look[-1] != self.evilKnight['id']:
                dead_id.append(self.witch['id'])
            else:
                dead_id.append(self.poison[-1])
        # 更新死亡信息
        dead_id = set(dead_id)
        for id in dead_id:
            self.player[id]['isLive'] = False
        if len(dead_id) == 0:
            results = "昨天晚上是平安夜\n"
        else:
            results = "昨天晚上 " + '号,'.join([str(id) for id in dead_id]) + '号 玩家阵亡, 没有遗言。\n' 
        return flow + results

    def summaryOneDay(self):
        dead_id = []
        if self.whiteKill[-1] != 0:
            dead_id.append(self.whiteWolfKing['id'])
            dead_id.append(self.whiteKill[-1])
        else:
            dead_id.append(self.vote[-1])
        # 这里黑狼王白天被猎人带走，猎人白天被黑狼王带走的复杂情况，由面杀时决定
        if self.shot[-1] != 0:
            dead_id.append(self.shot[-1])
        if self.blackKill[-1] != 0:
            dead_id.append(self.blackKill[-1])
        dead_id = set(dead_id)
        # 更新死亡信息
        for id in dead_id:
            self.player[id]['isLive'] = False
        if len(dead_id) == 0:
            results = "白天无事\n"
        else:
            results = "白天 " + '号,'.join([str(id) for id in dead_id]) + '号 玩家出局。\n' 
        return results


class CMDGame(Game):
    def __init__(self):
        """
            Not Finished, UI is better to help God.
        """
        super().__init__()
        # special print
        self.speakShow = ('\033[1;34;43m', '\033[0m')
        self.recordShow = ('\033[1;34m', '\033[0m')
    
    def GodSay(self, s):
        print(self.speakShow[0] + s + self.speakShow[1], end='')

    def GodRecord(self, s, need_input=True):
        print(self.recordShow[0] + s + self.recordShow[1], end='')
        if need_input:
            return input()
        else:
            print()
            return None

    def start(self):
        n = self.GodRecord("请输入玩家人数：")
        while n.isdigit() is False:
            n = self.GodRecord("请输入玩家人数(请输入数字)：")
        self.n = int(n)
        self.player = [None] * (self.n + 1)
        self.isKillSide = self.GodRecord("请输入是否是屠边局(1表示是/0表示否)：")
        self.isKillSide = True if int(self.isKillSide) != 0 else False

    def firstNight(self):
        self.GodSay(self.sentence[0])
        print()
        self.GodSay(self.sentence[1])
        print()

        # 狼人确认阶段
        wolf_str = self.GodRecord("请输入狼人的编号，以空格分隔：")
        while wolf_str == '':
            wolf_str = self.GodRecord("请输入狼人的编号，以空格分隔：")
        wolf_str = " ".join(wolf_str.strip().split())  # delete multiple space
        wolf_ids = wolf_str.split(' ')
        for id in wolf_ids:
            wolf = {'id': int(id), 'name': '狼人', 'isLive': True}
            self.wolf.append(wolf)
            self.player[int(id)] = wolf
        self.GodRecord("当前狼人为：" + " ".join([str(w['id']) for w in self.wolf]), False)

        # 狼人杀人阶段
        self.GodSay(self.sentence[2])
        print()
        id = self.GodRecord("请输入狼人击杀目标编号：")
        while id.isdigit() is False:
            id = self.GodRecord("请输入狼人击杀目标编号(请输入数字)：")
        self.kill.append(int(id))
        self.GodRecord("今晚狼人击杀目标：" + str(self.kill[-1]), False)

        # 预言家阶段
        self.GodSay(self.sentence[3])
        print()
        id = self.GodRecord("请输入预言家编号：")
        while id.isdigit() is False:
            id = self.GodRecord("请输入预言家编号(请输入数字)：")
        self.predictor['id'] = int(id)
        self.predictor['isLive'] = True
        self.player[int(id)] = self.predictor
        self.GodSay(self.sentence[4])
        print()
        id = self.GodRecord("请输入预言家查验目标编号：")
        while id.isdigit() is False:
            id = self.GodRecord("请输入预言家查验目标编号(请输入数字)：")
        self.look.append(int(id))
        self.GodRecord("今晚预言家查验目标：" + str(self.look[-1]), False)

        # 女巫阶段
        self.GodSay(self.sentence[5])
        print()
        id = self.GodRecord("请输入女巫编号：")
        while id.isdigit() is False:
            id = self.GodRecord("请输入女巫编号(请输入数字)：")
        self.witch['id'] = int(id)
        self.witch['isLive'] = True
        self.player[int(id)] = self.witch
        self.GodSay(self.sentence[6])
        print()
        if self.witch['save'] == 1:
            isSave = self.GodRecord("请输入女巫是否使用解药(使用为1，没使用为0)：")
            isSave = int(isSave)
            self.save.append(isSave)
            if isSave:
                self.poison.append(0)  # 毒药解药不能同一晚使用

            else:
                isPoison = self.GodRecord("请输入女巫是否使用毒药(使用则输入毒的目标编号，没使用为0)：")
                self.poison.append(int(isPoison))
        else:
            self.save.append(0)
            if self.witch['poison'] == 1:
                isPoison = self.GodRecord("请输入女巫是否使用毒药(使用则输入毒的目标编号，没使用为0)：")
                self.poison.append(int(isPoison))
            else:
                self.poison.append(0)
        beKilledPlayer = self.player[self.kill[-1]]
        s = ""
        if self.witch['save'] == 0:
            s += "女巫今晚没有解药"
        elif self.save[-1] == 1:
            s += "女巫今晚救了 " + str(beKilledPlayer['id']) + ' 号'
        else:
            s += "女巫今晚没有使用解药"
        s += '\n'
        if self.witch['poison'] == 0:
            s += "女巫今晚没有毒药"
        elif self.poison[-1] != 0:
            s += "女巫今晚毒了" + str(self.poison[-1]) + '号'
        else:
            s += "女巫今晚没有使用毒药"
        self.GodRecord(s, False)
        if self.save[-1] == 1:
            self.witch['save'] = 0
        if self.poison[-1] != 0:
            self.witch['poison'] = 0

        # 猎人阶段
        self.GodSay(self.sentence[7])
        print()
        id = self.GodRecord("请输入猎人编号：")
        while id.isdigit() is False:
            id = self.GodRecord("请输入猎人编号(请输入数字)：")
        self.hunter['id'] = int(id)
        self.hunter['isLive'] = True
        self.player[int(id)] = self.hunter
        self.GodSay(self.sentence[8])
        print()
        if self.poison[-1] != self.hunter["id"] and self.kill[-1] == self.hunter["id"] and self.save[-1] is not 1:
            self.hunter['canShot'] = True
            id = self.GodRecord("请输入狼人开枪目标编号, 不开枪请输入0：")
            while id.isdigit() is False:
                id = self.GodRecord("请输入狼人开枪目标编号, 不开枪请输入0(请输入数字)：")
            self.shot.append(int(id))
        else:
            self.shot.append(0)
        # 天亮了
        self.GodSay(self.sentence[9])
        print()
        for i, p in enumerate(self.player):
            if i != 0 and p is None:
                self.player[i] = {'id': 0, 'name': '平民', 'isLive': True}

    def Night(self):
        self.GodSay(self.sentence[0])
        print()
        self.GodSay(self.sentence[1])
        print()

        # 狼人杀人阶段
        self.GodSay(self.sentence[2])
        print()
        id = self.GodRecord("请输入狼人击杀目标编号：")
        while id.isdigit() is False:
            id = self.GodRecord("请输入狼人击杀目标编号(请输入数字)：")
        self.kill.append(int(id))
        self.GodRecord("今晚狼人击杀目标：" + str(self.kill[-1]), False)

        # 预言家阶段
        self.GodSay(self.sentence[3])
        self.GodSay(self.sentence[4])
        print()
        id = self.GodRecord("请输入预言家查验目标编号：")
        while id.isdigit() is False:
            id = self.GodRecord("请输入预言家查验目标编号(请输入数字)：")
        self.look.append(int(id))
        self.GodRecord("今晚预言家查验目标：" + str(self.look[-1]), False)

        # 女巫阶段
        self.GodSay(self.sentence[5])
        self.GodSay(self.sentence[6])
        print()
        if self.witch['save'] == 1:
            isSave = self.GodRecord("请输入女巫是否使用解药(使用为1，没使用为0)：")
            isSave = int(isSave)
            self.save.append(isSave)
            if isSave:
                self.poison.append(0)  # 毒药解药不能同一晚使用

            else:
                isPoison = self.GodRecord("请输入女巫是否使用毒药(使用则输入毒的目标编号，没使用为0)：")
                self.poison.append(int(isPoison))
        else:
            self.save.append(0)
            if self.witch['poison'] == 1:
                isPoison = self.GodRecord("请输入女巫是否使用毒药(使用则输入毒的目标编号，没使用为0)：")
                self.poison.append(int(isPoison))
            else:
                self.poison.append(0)
        beKilledPlayer = self.player[self.kill[-1]]
        s = ""
        if self.witch['save'] == 0:
            s += "女巫今晚没有解药"
        elif self.save[-1] == 1:
            s += "女巫今晚救了 " + str(beKilledPlayer['id']) + ' 号'
        else:
            s += "女巫今晚没有使用解药"
        s += '\n'
        if self.witch['poison'] == 0:
            s += "女巫今晚没有毒药"
        elif self.poison[-1] != 0:
            s += "女巫今晚毒了" + str(self.poison[-1]) + '号'
        else:
            s += "女巫今晚没有使用毒药"
        self.GodRecord(s, False)
        if self.save[-1] == 1:
            self.witch['save'] = 0
        if self.poison[-1] != 0:
            self.witch['poison'] = 0

        # 猎人阶段
        self.GodSay(self.sentence[7])
        self.GodSay(self.sentence[8])
        print()
        if self.poison[-1] != self.hunter["id"] and self.kill[-1] == self.hunter["id"] and self.save[-1] is not 1:
            self.hunter['canShot'] = True
            id = self.GodRecord("请输入狼人开枪目标编号, 不开枪请输入0：")
            while id.isdigit() is False:
                id = self.GodRecord("请输入狼人开枪目标编号, 不开枪请输入0(请输入数字)：")
            self.shot.append(int(id))
        else:
            self.shot.append(0)
        # 天亮了
        self.GodSay(self.sentence[9])
        print()
        for i, p in enumerate(self.player):
            if i != 0 and p is None:
                self.player[i] = {'id': 0, 'name': '平民', 'isLive': True}

    def summaryOneNight(self):
        dead_id = []
        if self.shot[-1] is not 0:
            dead_id.append(self.shot[-1])
        if self.save[-1] is not 1:
            dead_id.append(self.kill[-1])
        if self.poison[-1] is not 0:
            dead_id.append(self.poison[-1])
        for id in dead_id:
            self.player[id]['isLive'] = False
        dead_id = set(dead_id)
        if len(dead_id) > 0:
            self.GodSay("昨天晚上 " + "号".join([str(id) for id in dead_id]) + "号 玩家死亡")
        else:
            self.GodSay("昨天晚上是平安夜")

    def Day(self):
        id = self.GodRecord("准备输入白天票决的玩家编号：")
        while id.isdigit() is False:
            id = self.GodRecord("准备输入白天票决的玩家编号：(请输入数字)：")
        self.player[int(id)]['isLive'] = False


if __name__ == '__main__':
    g = CMDGame()
    g.start()
    g.firstNight()
    g.summaryOneNight()
    g.Day()


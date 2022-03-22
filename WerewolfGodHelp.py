import imp
import sys

from numpy import lookfor
import WerewolfGodHelpUI
from WerewolfGame import Game
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QStringListModel
import qdarkstyle
from qdarkstyle.dark.palette import DarkPalette  # noqa: E402
from qdarkstyle.light.palette import LightPalette  # noqa: E402
from functools import partial


def init(ui, game):
    player = game.playerNames
    for p in player:
        ui.comboBox.addItem(p)
        ui.comboBox_2.addItem(p)
        ui.comboBox_3.addItem(p)
        ui.comboBox_4.addItem(p)
        ui.comboBox_5.addItem(p)
        ui.comboBox_6.addItem(p)
        ui.comboBox_7.addItem(p)
        ui.comboBox_8.addItem(p)
    ui.textBrowser.setText("-------第1天-------\n")


def nightSummary(app, ui, game):
    """结算夜晚，并输出， 主题变白天"""
    # 改变主题和按钮状态
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=LightPalette))
    ui.pushButton_2.setEnabled(True)
    ui.pushButton.setEnabled(False)
    # 根据ui夜晚结果更新game
    kill = int(ui.spinBox.value())
    look = int(ui.spinBox_2.value())
    save = ui.checkBox.isChecked()
    usePoison = ui.checkBox_2.isChecked()
    poison = int(ui.spinBox_3.value())
    guard = int(ui.spinBox_6.value())
    canShot = ui.checkBox_3.isChecked()
    shot = int(ui.spinBox_7.value())
    blackKillOk = ui.checkBox_4.isChecked()
    blackKill = int(ui.spinBox_11.value())

    game.kill.append(kill)
    game.look.append(look)
    game.save.append(save)
    game.poison.append(poison)
    game.protect.append(guard)
    game.shot.append(shot)
    game.blackKill.append(blackKill)
    game.whiteKill.append(0)
    if look == game.whiteWolfKing['id'] and game.evilKnight['canRebound'] == True:
        game.evilKill.append(game.predictor['id'])
    elif poison == game.whiteWolfKing['id'] and game.evilKnight['canRebound'] == True:
        game.evilKill.append(game.witch['id'])
    else:
        game.evilKill.append(0)
    game.vote.append(0)
    print("狼刀", kill, "预查", look, "女巫救", save, "女巫毒",usePoison, poison, "守卫守", guard, "猎人枪", canShot, shot, "黑狼杀", blackKillOk, blackKill, "恶灵反", game.evilKill[-1])
    # 根据game总结这一晚的结果, 更新game的存活信息
    text = game.summaryOneNight()
    # 输出至右边textBrowser中
    ui.textBrowser.setText(ui.textBrowser.toPlainText() + text + '\n')
    # 把白天部分的UI根据game更新
    ui.spinBox_8.setValue(0)
    if game.whiteWolfKing['isLive'] is False:
        ui.spinBox_8.setEnabled(False)
    ui.spinBox_10.setValue(0)
    ui.spinBox_12.setValue(0)
    if game.hunter['isLive'] is False:
        ui.spinBox_12.setEnabled(False)
    ui.spinBox_9.setValue(0)
    if game.blackWolfKing['isLive'] is False:
        ui.spinBox_9.setEnabled(False)
    pass
    # 判定是否游戏结束
    if game.isEnd() == 1:
        ui.textBrowser.setText(ui.textBrowser.toPlainText() + "游戏结束，好人胜利!\n")
    elif game.isEnd() == -1:
        ui.textBrowser.setText(ui.textBrowser.toPlainText() + "游戏结束，狼人胜利!\n")
    else:
        pass


def updateHunter(ui, game):
    """只涉及黑夜猎人能否开枪，白天阶段后知道猎人生死"""
    kill = int(ui.spinBox.value())
    save = ui.checkBox.isChecked()
    usePoison = ui.checkBox_2.isChecked()
    poison = int(ui.spinBox_3.value())
    guard = int(ui.spinBox_6.value())
    hunterId = game.hunter['id']
    game.hunter['canShot'] = False
    hunterIsLive = game.hunter['isLive']
    if hunterIsLive:
        if kill is hunterId:
            game.hunter['canShot'] = True
            if save is True and guard != hunterId:
                game.hunter['canShot'] = False
            elif save is False and guard == hunterId:
                game.hunter['canShot'] = False
            elif save is True and guard == hunterId:
                # 女巫救和守卫守同时发生，暂定能开枪
                game.hunter['canShot'] = True
            else:
                game.hunter['canShot'] = True

    if game.hunter['canShot'] is True:
        ui.checkBox_3.setChecked(True)
        ui.spinBox_7.setEnabled(True)
    else:
        ui.checkBox_3.setChecked(False)
        ui.spinBox_7.setEnabled(False)
    print("狼刀", kill, "女巫救", save, "女巫毒",usePoison, poison, "守卫守", guard, "猎人枪", game.hunter['canShot'])


def updateBlackWolf(ui, game):
    kill = int(ui.spinBox.value())
    save = ui.checkBox.isChecked()
    usePoison = ui.checkBox_2.isChecked()
    poison = int(ui.spinBox_3.value())
    guard = int(ui.spinBox_6.value())
    shot = int(ui.spinBox_7.value())
    
    blackWolfId = game.blackWolfKing['id']
    game.blackWolfKing['canKill'] = False
    if game.blackWolfKing['isLive']:
        if kill == blackWolfId:
            game.blackWolfKing['canKill'] = True
            if save is True and guard != blackWolfId:
                game.blackWolfKing['canKill'] = False
            elif save is False and guard == blackWolfId:
                game.blackWolfKing['canKill'] = False
            elif save is True and guard == blackWolfId:
                # 女巫救和守卫守同时发生，暂定能发动技能
                game.blackWolfKing['canKill'] = True
            else:
                game.blackWolfKing['canKill'] = True
        if shot == blackWolfId:
            game.blackWolfKing['canKill'] = True

    if game.blackWolfKing['canKill'] is True:
        ui.checkBox_4.setChecked(True)
        ui.spinBox_11.setEnabled(True)
    else:
        ui.checkBox_4.setChecked(False)
        ui.spinBox_11.setEnabled(False)
    print("狼刀", kill, "女巫救", save, "女巫毒",usePoison, poison, "守卫守", guard, "黑狼王技能", game.blackWolfKing['canKill'])


def daySummary(app, ui, game):
    """结算白天，并输出， 主题变黑夜"""
    # 改变主题和按钮状态
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=DarkPalette))
    ui.pushButton_2.setEnabled(False)
    ui.pushButton.setEnabled(True)
    # 根据ui白天结果更新game
    whiteKill = int(ui.spinBox_8.value())
    vote = int(ui.spinBox_10.value())
    shot = int(ui.spinBox_12.value())
    blackKill = int(ui.spinBox_9.value())

    game.kill.append(0)
    game.look.append(0)
    game.save.append(False)
    game.poison.append(0)
    game.protect.append(0)
    game.shot.append(shot)
    game.blackKill.append(blackKill)
    game.whiteKill.append(whiteKill)
    game.evilKill.append(0)
    game.vote.append(vote)
    # 根据game总结白天的结果
    text = game.summaryOneDay()
    # 输出至右边textBrowser中
    ui.textBrowser.setText(ui.textBrowser.toPlainText() + text + '\n')
    # 在ui初始化黑夜部分, 女巫的毒解药是否可用
    ui.spinBox.setValue(0)
    ui.spinBox_2.setValue(0)
    if game.predictor['isLive'] is False:
        ui.spinBox_2.setEnabled(False)
    if game.witch['isLive']:
        ui.checkBox.setChecked(False)
        if game.witch['save'] == 1:
            ui.checkBox.setEnabled(True)
        else:
            ui.checkBox.setEnabled(False)
        
        ui.checkBox_2.setChecked(False)
        if game.witch['poison'] == 1:
            ui.checkBox_2.setEnabled(True)
        else:
            ui.checkBox_2.setEnabled(False)
        
        ui.spinBox_3.setValue(0)
        if game.witch['poison'] == 1:
            ui.spinBox_3.setEnabled(True)
        else:
            ui.spinBox_3.setEnabled(False)
    else:
        ui.checkBox.setChecked(False)
        ui.checkBox.setEnabled(False)
        ui.checkBox_2.setChecked(False)
        ui.checkBox_2.setEnabled(False)
        ui.spinBox_3.setValue(0)
        ui.spinBox_3.setEnabled(False)
    ui.spinBox_6.setValue(0)
    if game.guard['isLive'] is False:
        ui.spinBox_6.setEnabled(False)
    # 猎人和黑狼王进入黑天时先无效
    ui.checkBox_3.setChecked(False)
    ui.checkBox_3.setEnabled(False)
    ui.spinBox_7.setValue(0)
    ui.spinBox_7.setEnabled(False)
    ui.checkBox_4.setChecked(False)
    ui.checkBox_4.setEnabled(False)
    ui.spinBox_11.setValue(0)
    ui.spinBox_11.setEnabled(False)
    # 判定是否游戏结束
    if game.isEnd() == 1:
        ui.textBrowser.setText(ui.textBrowser.toPlainText() +"游戏结束，好人胜利!\n")
    elif game.isEnd() == -1:
        ui.textBrowser.setText(ui.textBrowser.toPlainText() +"游戏结束，狼人胜利!\n")
    else:
        game.dayNum += 1
        ui.textBrowser.setText(ui.textBrowser.toPlainText() +"-------第" + str(game.dayNum) + "天-------\n")


def setPlayer(ui, game):
    """更新玩家编号"""
    current_players = []
    current_players.append(ui.comboBox.currentText())
    current_players.append(ui.comboBox_2.currentText())
    current_players.append(ui.comboBox_3.currentText())
    current_players.append(ui.comboBox_4.currentText())
    current_players.append(ui.comboBox_5.currentText())
    current_players.append(ui.comboBox_6.currentText())
    current_players.append(ui.comboBox_7.currentText())
    current_players.append(ui.comboBox_8.currentText())
    ["请选择", "白狼王", "黑狼王", "恶灵骑士", "预言家", "女巫", "守卫", "猎人", "白痴"]
    for i, p in enumerate(current_players):
        id = i + 1
        if p == "请选择":
            pass
        elif p == "白狼王":
            game.whiteWolfKing['id'] = id
            game.player[id] = game.whiteWolfKing
        elif p == "黑狼王":
            game.blackWolfKing['id'] = id
            game.player[id] = game.blackWolfKing
        elif p == "恶灵骑士":
            game.evilKnight['id'] = id
            game.player[id] = game.evilKnight
        elif p == "预言家":
            game.predictor['id'] = id
            game.player[id] = game.predictor
        elif p == "女巫":
            game.witch['id'] = id
            game.player[id] = game.witch
        elif p == "守卫":
            game.guard['id'] = id
            game.player[id] = game.guard
        elif p == "猎人":
            game.hunter['id'] = id
            game.player[id] = game.hunter
        elif p == "白痴":
            game.idiot['id'] = id
            game.player[id] = game.idiot
    print([p['name'] if p is not None else '未确定' for p in game.player])


def QTMain():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=DarkPalette))
    ui = WerewolfGodHelpUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    game = Game()
    init(ui, game)
    ui.pushButton_2.setEnabled(False)
    ui.pushButton.clicked.connect(partial(nightSummary, app, ui, game))
    ui.pushButton_2.clicked.connect(partial(daySummary, app, ui, game))
    ui.pushButton_3.clicked.connect(partial(updateHunter, ui, game))
    ui.pushButton_4.clicked.connect(partial(updateBlackWolf, ui, game))
    # 当左边栏选择一个身份后就更新game里玩家的编号信息
    ui.comboBox.currentIndexChanged.connect(partial(setPlayer, ui, game))
    ui.comboBox_2.currentIndexChanged.connect(partial(setPlayer, ui, game))
    ui.comboBox_3.currentIndexChanged.connect(partial(setPlayer, ui, game))
    ui.comboBox_4.currentIndexChanged.connect(partial(setPlayer, ui, game))
    ui.comboBox_5.currentIndexChanged.connect(partial(setPlayer, ui, game))
    ui.comboBox_6.currentIndexChanged.connect(partial(setPlayer, ui, game))
    ui.comboBox_7.currentIndexChanged.connect(partial(setPlayer, ui, game))
    ui.comboBox_8.currentIndexChanged.connect(partial(setPlayer, ui, game))
    sys.exit(app.exec_())

QTMain()

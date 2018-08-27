import player11
import threading
import numpy as np

from collections import deque


class Player12(player11.Player11, threading.Thread):
    def __init__(self):
        super(Player12, self).__init__()
        self.name = "Crespo"
        # =============for machine learning
        # 入力値分割数
        self.num_digitized = 6
        self.goal_average_reward = 195  # この報酬を超えると学習終了（中心への制御なし）
        # 出力数
        self.action_num = 7
        self.action = 0
        self.actions = ("(turn 0)", "(turn 60)", "(turn -60)", "(dash 100)", "(dash -100)", "(kick 100 0)", "(kick 50 0)")


    # 実行
    def play_0(self):
        command = "(turn 0)"
        if self.checkInitialMode():
            if self.checkInitialMode():
                self.setKickOffPosition()
                command = \
                    "(move " + str(self.m_dKickOffX) + " " + str(self.m_dKickOffY) + ")"
                self.m_strCommand[self.m_iTime] = command
        else:
            # (コマンド生成)===================
            self.m_strCommand[self.m_iTime] = command
            # ==================================

    def analyzeMessage(self, message):
        # 初期メッセージの処理
        # print("p11:message:", message)
        if message.startswith("(init "):
            self.analyzeInitialMessage(message)
        # 視覚メッセージの処理
        elif message.startswith("(see "):
            self.analyzeVisualMessage(message)
        # 体調メッセージの処理
        elif message.startswith("(sense_body "):
            self.analyzePhysicalMessage(message)
            if self.m_iVisualTime < self.m_iTime:
                self.predict(self.m_iVisualTime, self.m_iTime)
            self.play_0()
            self.send(self.m_strCommand[self.m_iTime])
        # 聴覚メッセージの処理
        elif message.startswith("(hear "):
            self.analyzeAuralMessage(message)
        # サーバパラメータの処理
        elif message.startswith("(server_param"):
            self.analyzeServerParam(message)
        # プレーヤーパラメータの処理
        elif message.startswith("(player_param"):
            self.analyzePlayerParam(message)
        # プレーヤータイプの処理
        elif message.startswith("(player_type"):
            self.analyzePlayerType(message)
            # print("player_type_message", message)
        # エラーの処理
        else:
            print("p11 サーバーからエラーが伝えられた:", message)
            print("p11 エラー発生原因のコマンドは右記の通り :", self.m_strCommand[self.m_iTime])


    def start_selfplay(self):



if __name__ == "__main__":
    plays = []
    for i in range(4):
        p = Player12()
        plays.append(p)
        teamname = str(p.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        plays[i].initialize((i % 2 + 1), teamname, "localhost", 6000)
        plays[i].start()

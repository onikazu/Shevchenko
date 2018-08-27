class TrainPipeline():
    def __init__(self):
        self.game_batch_num = 100
        self.play_batch_size = 512 # 512試合を100回訓練

    def collect_selfplay_data(self, n_games=1):
        """
        1バッチ分の処理、訓練
        :param n_games: バッチ長
        :return: none
        """
        for i in range(n_games):  # 結果を集める
            winner, play_data = self.game.start_self_play(self.mcts_player,
                                                          temp=self.temp)
            play_data = list(play_data)[:]
            self.episode_len = len(play_data)
            # augment the data
            play_data = self.get_equi_data(play_data)
            self.data_buffer.extend(play_data)




    def run(self):
        """
        訓練させる
        :return:none
        """
        try:
            for i in range(self.game_batch_num):  # 集めた結果を回す
                self.collect_selfplay_data(self.play_batch_size)  # エピソードの繰り返し
                print("batch i:{}, episode_len:{}".format(
                    i + 1, self.episode_len))  # 最後の試合の勝敗つくまでのステップ数？
                if len(self.data_buffer) > self.batch_size:  # まだ性能に余裕あれば？
                    loss, entropy = self.policy_update()  # 更新（まだモデルにコミットはしていない）
                # check the performance of the current model,
                # and save the model params
                if (i + 1) % self.check_freq == 0:
                    print("current self-play batch: {}".format(i + 1))
                    win_ratio = self.policy_evaluate()
                    self.policy_value_net.save_model('./current_policy.model')  # 今回の学習のコミット（ベストでなくてもおｋ）
                    if win_ratio > self.best_win_ratio:
                        print("New best policy!!!!!!!!")
                        self.best_win_ratio = win_ratio
                        # update the best_policy
                        self.policy_value_net.save_model('./best_policy.model')　  # ベストコミット
                        if (self.best_win_ratio == 1.0 and
                                self.pure_mcts_playout_num < 5000):
                            self.pure_mcts_playout_num += 1000
                            self.best_win_ratio = 0.0
        except KeyboardInterrupt:
            print('\n\rquit')


if __name__ == "__main__":
    train_pipeline = TrainPipeline()
    train_pipeline.run()
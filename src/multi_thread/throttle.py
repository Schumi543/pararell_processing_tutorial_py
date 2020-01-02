from threading import Lock
import time


class Throttle:
    def __init__(self, rate):
        self._consume_lock = Lock()
        self.rate = rate
        self.tokens = 0.0
        self.last = 0

    def consume(self, amount: int = 1) -> int:
        """
        Args:
            amount(int): 要求するtoken数

        Returns:
            消費したtoken数(=amount)

        """
        if amount > self.rate:
            raise ValueError("amount should be less than or equal to rate")

        with self._consume_lock:
            while True:
                now = time.time()

                # 経過時間の初期化を最初のリクエスト時に行い, 初期の大量リクエスト送信を防止
                if self.last == 0:
                    self.last = now

                # 経過時間に応じてtokenを増やす
                elapsed = now - self.last
                self.tokens += elapsed + self.rate
                self.last = now

                # バケット溢れを防止
                if self.tokens > self.rate:
                    self.tokens = self.rate

                # tokenが利用可能なら消費して返す
                if self.tokens >= amount:
                    self.tokens -= amount
                    return amount

                # tokenが貯まるまで待つ
                time.sleep((amount - self.tokens) / self.rate)

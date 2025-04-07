# models/trainer.py

import torch
import torch.nn.functional as F

class Trainer:
    def __init__(self, model, lr=3e-4, gamma=0.7, use_critic=True):
        self.current_episode = 0
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        self.gamma = gamma
        self.trajectory = []
        self.debug_log = []

        self.use_critic = use_critic  # 💡 ВОТ ОН

    def record_step(self, inputs, action_idx, value, reward, logits):
        self.trajectory.append((inputs, action_idx, value, reward, logits))

    def clear(self):
        self.trajectory = []

    # Обновлённая версия train_from_trajectory с N-step return

    def train_from_trajectory_n_step(self, n_steps=10):
        self.current_episode += 1

        policy_loss = 0
        value_loss = 0
        entropy_total = 0

        trajectory_len = len(self.trajectory)

        for i in range(trajectory_len):
            R = 0
            discount = 1.0
            for j in range(i, min(i + n_steps, trajectory_len)):
                _, _, _, reward, _ = self.trajectory[j]
                if isinstance(reward, torch.Tensor):
                    reward = reward.item()
                R += discount * reward
                discount *= self.gamma

            # bootstrap value at the end
            if i + n_steps < trajectory_len:
                next_inputs, *_ = self.trajectory[i + n_steps]
                with torch.no_grad():
                    _, next_value, _ = self.model(next_inputs)
                    R += discount * next_value.item()

            inputs, action_idx, _, _, logits = self.trajectory[i]
            logits = self.model(inputs)[0]  # ← это из model возвращается (logits, value, hidden)
            _, value_pred, _ = self.model(inputs)

            log_probs = F.log_softmax(logits, dim=1)
            probs = torch.softmax(logits, dim=1)
            log_prob = log_probs[0, action_idx]
            entropy = -torch.sum(probs * log_probs)
            entropy_total += entropy

            if self.use_critic:
                advantage = R - value_pred.item()
                policy_loss += -log_prob * advantage
                value_target = torch.tensor([[R]], dtype=torch.float32)
                value_loss += F.mse_loss(value_pred, value_target)
            else:
                R_tensor = torch.tensor(R, dtype=torch.float32, device=logits.device)
                policy_loss += -log_prob * R_tensor

                value_loss += torch.tensor(0.0, device=logits.device)

                advantage = R  # Просто для дебага

            self.debug_log.append({
                "episode": self.current_episode,
                "step": i,
                "value_pred": value_pred.item(),
                "target": R,
                "advantage": advantage,
                "action": action_idx,
            })

        total_loss = policy_loss + 0.5 * value_loss - 0.01 * entropy_total

        self.optimizer.zero_grad()
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
        self.optimizer.step()
        self.clear()

        print(f"[TRAIN n-step] loss: {total_loss.item():.4f} | steps: {trajectory_len}")


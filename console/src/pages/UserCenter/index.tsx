import { Avatar, Card, Descriptions, Tag } from "antd";
import { useMemo } from "react";
import { PageHeader } from "@/components/PageHeader";
import { USER_PROFILE } from "@/constants/userProfile";
import { useAgentStore } from "@/stores/agentStore";
import styles from "./index.module.less";

export default function UserCenterPage() {
  const { selectedAgent, agents } = useAgentStore();

  const currentAgent = useMemo(
    () => agents.find((agent) => agent.id === selectedAgent),
    [agents, selectedAgent],
  );

  return (
    <div className={styles.userCenterPage}>
      <PageHeader parent="个人工作台" current="用户中心" />

      <div className={styles.content}>
        <Card className={styles.heroCard} bordered={false}>
          <div className={styles.hero}>
            <Avatar
              src={USER_PROFILE.avatar}
              size={88}
              className={styles.heroAvatar}
            />
            <div className={styles.heroCopy}>
              <div className={styles.heroTitleRow}>
                <h1 className={styles.heroTitle}>{USER_PROFILE.name}</h1>
                <Tag color="blue" className={styles.heroTag}>
                  {USER_PROFILE.organization}
                </Tag>
              </div>
              <p className={styles.heroSubtitle}>
                {USER_PROFILE.company} · {USER_PROFILE.title}
              </p>
              <p className={styles.heroDesc}>
                负责企业级智能体的落地、运营与协同，聚焦数字业务场景下的应用接入与体验优化。
              </p>
            </div>
          </div>
        </Card>

        <div className={styles.grid}>
          <Card className={styles.infoCard} bordered={false} title="基础信息">
            <Descriptions
              column={1}
              labelStyle={{ width: 112 }}
              className={styles.descriptions}
            >
              <Descriptions.Item label="姓名">
                {USER_PROFILE.name}
              </Descriptions.Item>
              <Descriptions.Item label="所在公司">
                {USER_PROFILE.company}
              </Descriptions.Item>
              <Descriptions.Item label="所在组织">
                {USER_PROFILE.organization}
              </Descriptions.Item>
              <Descriptions.Item label="岗位">
                {USER_PROFILE.title}
              </Descriptions.Item>
              <Descriptions.Item label="员工编号">
                {USER_PROFILE.employeeId}
              </Descriptions.Item>
            </Descriptions>
          </Card>

          <Card className={styles.infoCard} bordered={false} title="联系信息">
            <Descriptions
              column={1}
              labelStyle={{ width: 112 }}
              className={styles.descriptions}
            >
              <Descriptions.Item label="邮箱">
                {USER_PROFILE.email}
              </Descriptions.Item>
              <Descriptions.Item label="电话">
                {USER_PROFILE.phone}
              </Descriptions.Item>
              <Descriptions.Item label="办公地">
                {USER_PROFILE.location}
              </Descriptions.Item>
              <Descriptions.Item label="账号状态">
                <Tag color="green">正常</Tag>
              </Descriptions.Item>
            </Descriptions>
          </Card>

          <Card
            className={`${styles.infoCard} ${styles.agentCard}`}
            bordered={false}
            title="智能体信息"
          >
            <Descriptions
              column={1}
              labelStyle={{ width: 112 }}
              className={styles.descriptions}
            >
              <Descriptions.Item label="智能体 ID">
                <span className={styles.monoText}>{selectedAgent || "default"}</span>
              </Descriptions.Item>
              <Descriptions.Item label="智能体名称">
                {currentAgent?.name || "默认智能体"}
              </Descriptions.Item>
              <Descriptions.Item label="描述">
                {currentAgent?.description || "当前未配置额外描述信息"}
              </Descriptions.Item>
              <Descriptions.Item label="工作目录">
                <span className={styles.monoText}>
                  {currentAgent?.workspace_dir || "~/.qwenpaw/workspaces/default"}
                </span>
              </Descriptions.Item>
              <Descriptions.Item label="启用状态">
                <Tag color={currentAgent?.enabled === false ? "red" : "green"}>
                  {currentAgent?.enabled === false ? "已停用" : "运行中"}
                </Tag>
              </Descriptions.Item>
            </Descriptions>
          </Card>
        </div>
      </div>
    </div>
  );
}

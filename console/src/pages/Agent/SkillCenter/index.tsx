import { BulbOutlined, RocketOutlined, SafetyOutlined } from "@ant-design/icons";
import { PageHeader } from "@/components/PageHeader";
import styles from "./index.module.less";

const skillCards = [
  {
    title: "智能检索",
    subtitle: "Knowledge Search",
    description:
      "连接文档、知识库和业务资料，快速返回结构化答案，适合规程查询与日常问答。",
    tags: ["RAG", "知识库", "检索增强"],
    accent: "cyan",
  },
  {
    title: "流程编排",
    subtitle: "Workflow Automation",
    description:
      "把固定动作整理成标准流程，支持任务分发、执行串联和结果回传，适合重复性办公场景。",
    tags: ["自动化", "流程", "提效"],
    accent: "blue",
  },
  {
    title: "多智能体协同",
    subtitle: "Multi-Agent",
    description:
      "让规划、执行、审校等角色分工协作，适合复杂任务拆解、多人业务支持与项目推进。",
    tags: ["协作", "规划", "执行"],
    accent: "sky",
  },
  {
    title: "文档生产",
    subtitle: "Document Drafting",
    description:
      "支持通知、方案、周报和总结类内容的快速起草，统一风格并提升输出效率。",
    tags: ["公文", "写作", "模板"],
    accent: "ice",
  },
  {
    title: "数据分析",
    subtitle: "Data Insight",
    description:
      "面向表格和业务指标给出摘要、异常提示与趋势解读，帮助快速获得关键结论。",
    tags: ["分析", "报表", "洞察"],
    accent: "cyan",
  },
  {
    title: "安全审查",
    subtitle: "Guardrail Review",
    description:
      "提供输入检查、敏感信息识别和操作边界提醒，适合企业环境下的通用防护场景。",
    tags: ["安全", "审查", "合规"],
    accent: "blue",
  },
];

const highlights = [
  {
    icon: <BulbOutlined />,
    title: "静态样板页",
    text: "当前页面为静态技能展板，适合后续继续接入真实技能数据。",
  },
  {
    icon: <RocketOutlined />,
    title: "适合演示",
    text: "卡片布局适合做能力总览、产品展示和内部方案说明。",
  },
  {
    icon: <SafetyOutlined />,
    title: "易于扩展",
    text: "后续可以继续加筛选、详情抽屉、启用状态与分组标签。",
  },
];

export default function SkillCenterPage() {
  return (
    <div className={styles.page}>
      <PageHeader
        items={[{ title: "工作区" }, { title: "技能中心" }]}
        subRow={
          <div className={styles.subRow}>
            <span className={styles.subRowBadge}>Static Skills Gallery</span>
            <p className={styles.subRowText}>
              汇总展示通用智能体可承载的技能模块，用于概览、选型和后续扩展。
            </p>
          </div>
        }
      />

      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <p className={styles.eyebrow}>SKILL CENTER</p>
          <h1 className={styles.title}>苏电AI通用智能体技能中心</h1>
          <p className={styles.description}>
            一个面向企业通用场景的静态技能卡片页。这里展示的是能力清单，不依赖后端接口，便于先把展示层搭起来。
          </p>
        </div>
        <div className={styles.heroPanel}>
          {highlights.map((item) => (
            <div key={item.title} className={styles.highlightItem}>
              <span className={styles.highlightIcon}>{item.icon}</span>
              <div>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className={styles.grid}>
        {skillCards.map((card, index) => (
          <article
            key={card.title}
            className={`${styles.card} ${styles[`accent${card.accent}`]}`}
          >
            <div className={styles.cardGlow} />
            <div className={styles.cardHeader}>
              <div>
                <p className={styles.cardSubtitle}>{card.subtitle}</p>
                <h2>{card.title}</h2>
              </div>
              <span className={styles.cardIndex}>
                {String(index + 1).padStart(2, "0")}
              </span>
            </div>
            <p className={styles.cardDescription}>{card.description}</p>
            <div className={styles.tagRow}>
              {card.tags.map((tag) => (
                <span key={tag} className={styles.tag}>
                  {tag}
                </span>
              ))}
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}

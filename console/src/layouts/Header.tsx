import { Layout, Space, Avatar } from "antd";
import { useTranslation } from "react-i18next";
import styles from "./index.module.less";
import { useNavigate } from "react-router-dom";
import { USER_PROFILE } from "@/constants/userProfile";
import sdaiIconUrl from "../public/sdai.png";

const { Header: AntHeader } = Layout;

export default function Header() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <>
      <AntHeader className={styles.header}>
        <div className={styles.logoWrapper}>
          <img
            src={sdaiIconUrl}
            alt=""
            aria-hidden="true"
            className={styles.brandIcon}
          />
          <div className={styles.brandTextGroup}>
            <span className={styles.brandTitle}>通用智能体</span>
          </div>
          <div className={styles.logoDivider} />
        </div>
        <Space size="middle">
          <button
            type="button"
            className={styles.userEntry}
            onClick={() => navigate("/user-center")}
          >
            <Avatar
              src={USER_PROFILE.avatar}
              size={38}
              className={styles.userAvatar}
            />
            <span className={styles.userMeta}>
              <span className={styles.userName}>
                {`${USER_PROFILE.name}（${USER_PROFILE.organization}）`}
              </span>
              <span className={styles.userOrg}>{USER_PROFILE.company}</span>
            </span>
          </button>
          <div className={styles.headerDivider} />
        </Space>
      </AntHeader>
    </>
  );
}

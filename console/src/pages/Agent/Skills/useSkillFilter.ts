import { useMemo, useState } from "react";
import { SKILL_TAG_FILTER_PREFIX } from "@/constants/skill";

interface Filterable {
  name: string;
  description?: string;
  tags?: string[];
  source?: string;
}

type SkillTypeFilter = "all" | "builtin" | "custom";

export function useSkillFilter<T extends Filterable>(skills: T[]) {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchTags, setSearchTags] = useState<string[]>([]);
  const [skillType, setSkillType] = useState<SkillTypeFilter>("all");

  const allTags = useMemo(
    () => Array.from(new Set(skills.flatMap((s) => s.tags || []))).sort(),
    [skills],
  );

  const selectedTags = useMemo(
    () =>
      searchTags
        .filter((t) => t.startsWith(SKILL_TAG_FILTER_PREFIX))
        .map((t) => t.slice(SKILL_TAG_FILTER_PREFIX.length)),
    [searchTags],
  );

  const filteredSkills = useMemo(() => {
    const q = searchQuery.toLowerCase();
    return skills.filter((skill) => {
      const matchesText =
        !q ||
        skill.name.toLowerCase().includes(q) ||
        (skill.description || "").toLowerCase().includes(q);
      const matchesTag =
        selectedTags.length === 0 ||
        selectedTags.some((tag) => skill.tags?.includes(tag));
      const matchesType =
        skillType === "all" ||
        (skillType === "builtin" && skill.source === "builtin") ||
        (skillType === "custom" && skill.source !== "builtin");
      return matchesText && matchesTag && matchesType;
    });
  }, [skills, searchQuery, selectedTags, skillType]);

  return {
    searchQuery,
    setSearchQuery,
    searchTags,
    setSearchTags,
    skillType,
    setSkillType,
    allTags,
    filteredSkills,
  };
}

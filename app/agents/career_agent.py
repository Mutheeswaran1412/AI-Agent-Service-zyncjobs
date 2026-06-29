from typing import Optional
from .base_agent import BaseAgent
from app.prompts.prompt_manager import prompt_manager
from app.prompts.system_prompt import CAREER_SYSTEM_PROMPT
from app.tools.skill_extractor import SkillExtractorTool
from app.tools.keyword_tool import KeywordTool
from app.memory.memory_manager import memory


class CareerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="career_agent",
            description="Provides career advice, skill recommendations, and learning paths",
        )
        self.skill_extractor = SkillExtractorTool()
        self.keyword_tool = KeywordTool()

    def system_prompt(self) -> str:
        return CAREER_SYSTEM_PROMPT

    async def execute(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        history = memory.get_history(user_id) if user_id else []
        current_role = kwargs.get("current_role", "")
        target_role = kwargs.get("target_role", "")
        skills = kwargs.get("skills", [])

        if user_id:
            saved_skills = memory.get_skills(user_id)
            saved_goal = memory.get_goal(user_id)
            if not skills and saved_skills:
                skills = saved_skills
            if not target_role and saved_goal:
                target_role = saved_goal

        detected_skills = self.skill_extractor.run(query + " " + current_role + " " + target_role)
        all_skills = list(dict.fromkeys(list(skills) + detected_skills))

        enriched = f"""
Current Role: {current_role or 'Not specified'}
Target Role: {target_role or 'Not specified'}
Known Skills: {', '.join(all_skills) if all_skills else 'Not specified'}
"""
        prompt = prompt_manager.build_career_prompt(query + enriched, history)
        prompt = self.augment_with_context(prompt, query)
        response = await self.generate(prompt, system=CAREER_SYSTEM_PROMPT)

        if user_id:
            memory.store_message(user_id, "user", query)
            memory.store_message(user_id, "assistant", response)
            memory.store_skills(user_id, all_skills)
            if target_role:
                memory.store_goal(user_id, target_role)

        return {"advice": response}

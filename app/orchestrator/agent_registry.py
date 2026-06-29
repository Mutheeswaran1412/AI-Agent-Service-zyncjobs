def register_agents(master_agent):
    from app.agents.resume_agent import ResumeAgent
    from app.agents.career_agent import CareerAgent
    from app.agents.recruiter_agent import RecruiterAgent
    from app.agents.interview_agent import InterviewAgent
    from app.agents.job_match_agent import JobMatchAgent
    from app.agents.chat_agent import ChatAgent
    master_agent.register("resume", ResumeAgent())
    master_agent.register("career", CareerAgent())
    master_agent.register("recruiter", RecruiterAgent())
    master_agent.register("interview", InterviewAgent())
    master_agent.register("job_match", JobMatchAgent())
    master_agent.register("general", ChatAgent())

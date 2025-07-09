import re
from json_loader import load_problem
from model_processor import HuggingFaceModelProcessor 
PROBLEM_PATH = "data/problems" 
EDITORIAL_PATH = "data/editorials"

class ProblemChatbot:
    def __init__(self):
        self.model = HuggingFaceModelProcessor()  
        self.current_problem = None
        self.problem_data = None
        self.conversation_history = []

    def _extract_problem_id(self, text):
        """Extract problem ID with flexible formatting"""
        match = re.search(r'(\d{4}[A-Za-z])', text, re.IGNORECASE)
        return match.group(1).upper() if match else None
    
    def _load_problem(self, problem_id):
        """Load problem data with validation"""
        data = load_problem(problem_id, PROBLEM_PATH, EDITORIAL_PATH)
        if not data:
            raise ValueError(f"No data found for problem {problem_id}")
        return data
    
    def _build_context(self):
        """Build comprehensive problem context"""
        if not self.current_problem or not self.problem_data:
            return None
        
        return (
            f"Problem {self.current_problem}: {self.problem_data.get('title', 'Untitled')}\n"
            f"Statement: {self.problem_data.get('statement', '')}\n"
            f"Input Specification: {self.problem_data.get('input', '')}\n"
            f"Output Specification: {self.problem_data.get('output', '')}\n"
            f"Hint: {self.problem_data.get('hint', 'None provided')}\n"
            f"Solution Approach: {self.problem_data.get('solution', 'None provided')}"
        )
    
    def _build_system_message(self):
        """Create system message based on current state"""
        base_message = "You are a competitive programming assistant. "
        if self.current_problem and self.problem_data:
            return base_message + (
                f"Currently discussing problem {self.current_problem}. "
                f"Refer to the problem details when answering questions."
            )
        return base_message + "Ask the user to specify a problem ID to begin."

    def respond(self, user_input):
        """Handle user input with proper chat completion format"""
        user_input = user_input.strip()

        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        if any(greet in user_input.lower() for greet in ["hi", "hello", "hey"]):
            response = "Hello! I'm your competitive programming assistant. Please provide a problem ID (e.g., 2093I) to get started."
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            return response

        # Handle problem ID specification
        problem_id = self._extract_problem_id(user_input)
        if problem_id:
            try:
                self.current_problem = problem_id
                self.problem_data = self._load_problem(problem_id)
                response = f"Loaded problem {problem_id}. You can ask about:\n- The problem statement\n- Input/output specifications\n- Solution approach"
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                return response
            except ValueError as e:
                self.conversation_history.append({
                    "role": "assistant",
                    "content": str(e)
                })
                return str(e)
        
        if not self.current_problem:
            response = "Please first specify a problem ID (e.g., 2093I)."
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            return response
        
        context = self._build_context()
        prompt = user_input
        
        if "hint" in user_input.lower():
            prompt = (
                f"Provide a helpful hint for problem {self.current_problem} "
                f"without giving away the full solution. Problem details:\n{context}"
            )
        elif "solution" in user_input.lower() or "solve" in user_input.lower():
            prompt = (
                f"Explain the solution approach for problem {self.current_problem} "
                f"in a step-by-step manner. Include any important insights or algorithms needed. "
                f"Problem details:\n{context}"
            )
        elif "explain" in user_input.lower() or "how" in user_input.lower():
            prompt = (
                f"Explain how to approach solving problem {self.current_problem} "
                f"in simple terms suitable for a beginner. Problem details:\n{context}"
            )

        response = self.model.generate_response(
            prompt=prompt,
            conversation_history=self.conversation_history,
            system_message=self._build_system_message()
        )
    
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
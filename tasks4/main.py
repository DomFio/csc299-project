import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def summarize_task(description: str) -> str:
    """Summarize a task description using GPT-5-mini."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    completion = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant that summarizes tasks concisely."},
            {"role": "user", "content": f"Summarize this task in 5 words or less: {description}"}
        ]
    )
    
    return completion.choices[0].message.content


def main():
    """Main function - summarize multiple task descriptions."""
    
    # At least 2 paragraph-length task descriptions
    tasks = [
        """I need to complete some lawn work at my parents house. I need to rake all of the leaves in the yard.
        Then I have to mow the lawn and trim the hedges. 
        After that, I need to water the plants and flowers in the garden. 
        Finally, I have to clean up any debris and put away all of the lawn equipment.""",
        
        """Tomorrow before I start anything else, I need to go to the gym and work out my arms.
        go get a car wash and clean the inside of my car. I also need to go to the grocery store,
        and pick up some food for the week. After that, I have to stop by the post office to mail a package."""
    ]
    
    print("=" * 60)
    print("Task Summarizer using OpenAI API")
    print("=" * 60)
    print()
    
    # Loop through and summarize each task
    for i, task in enumerate(tasks, 1):
        print(f"Task {i}:")
        print(f"Description: {task[:80]}...")
        print("Summarizing...")
        
        summary = summarize_task(task)
        
        print(f"✨ Summary: {summary}")
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
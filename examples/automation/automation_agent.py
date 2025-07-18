"""
Task Automation Agent Example
Demonstrates workflow automation and task management capabilities
"""

import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class Task:
    id: str
    title: str
    description: str
    priority: Priority
    status: TaskStatus
    assigned_to: str
    created_date: datetime
    due_date: Optional[datetime]
    completed_date: Optional[datetime]
    dependencies: List[str]
    tags: List[str]
    estimated_duration: int  # minutes
    actual_duration: Optional[int]

class AutomationAgent:
    """
    An AI agent that automates workflows and manages tasks including:
    - Task scheduling and prioritization
    - Workflow automation
    - Email management
    - Calendar optimization
    - Report generation
    - Process monitoring
    """
    
    def __init__(self):
        self.tasks = {}
        self.workflows = {}
        self.automation_rules = []
        self.email_templates = {}
        self.calendar_events = []
        self.reports = []
        self.task_counter = 0
    
    def create_task(self, title: str, description: str, priority: Priority, 
                   assigned_to: str, due_date: Optional[datetime] = None,
                   dependencies: List[str] = None, tags: List[str] = None,
                   estimated_duration: int = 60) -> str:
        """Create a new task"""
        self.task_counter += 1
        task_id = f"TASK-{self.task_counter:04d}"
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING,
            assigned_to=assigned_to,
            created_date=datetime.now(),
            due_date=due_date,
            completed_date=None,
            dependencies=dependencies or [],
            tags=tags or [],
            estimated_duration=estimated_duration,
            actual_duration=None
        )
        
        self.tasks[task_id] = task
        return task_id
    
    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update task status and trigger automation rules"""
        if task_id not in self.tasks:
            return False
        
        old_status = self.tasks[task_id].status
        self.tasks[task_id].status = status
        
        if status == TaskStatus.COMPLETED:
            self.tasks[task_id].completed_date = datetime.now()
            # Calculate actual duration
            created = self.tasks[task_id].created_date
            self.tasks[task_id].actual_duration = int((datetime.now() - created).total_seconds() / 60)
        
        # Trigger automation rules
        self._trigger_automation_rules(task_id, old_status, status)
        
        return True
    
    def get_task_recommendations(self, user: str) -> List[Dict]:
        """Get AI-powered task recommendations for a user"""
        user_tasks = [task for task in self.tasks.values() if task.assigned_to == user]
        
        recommendations = []
        
        # Priority-based recommendations
        high_priority_tasks = [t for t in user_tasks if t.priority == Priority.HIGH and t.status == TaskStatus.PENDING]
        if high_priority_tasks:
            recommendations.append({
                'type': 'priority_focus',
                'message': f"You have {len(high_priority_tasks)} high-priority tasks pending",
                'tasks': [t.id for t in high_priority_tasks[:3]],
                'action': 'Focus on completing these high-priority tasks first'
            })
        
        # Overdue task recommendations
        overdue_tasks = [t for t in user_tasks if t.due_date and t.due_date < datetime.now() and t.status != TaskStatus.COMPLETED]
        if overdue_tasks:
            recommendations.append({
                'type': 'overdue_alert',
                'message': f"You have {len(overdue_tasks)} overdue tasks",
                'tasks': [t.id for t in overdue_tasks],
                'action': 'Immediate attention required for overdue tasks'
            })
        
        # Dependency recommendations
        ready_tasks = self._get_ready_tasks(user)
        if ready_tasks:
            recommendations.append({
                'type': 'dependency_ready',
                'message': f"{len(ready_tasks)} tasks are now ready to start",
                'tasks': [t.id for t in ready_tasks],
                'action': 'These tasks can be started as dependencies are completed'
            })
        
        # Workload balancing
        workload = self._calculate_user_workload(user)
        if workload['total_hours'] > 40:
            recommendations.append({
                'type': 'workload_warning',
                'message': f"Your workload is {workload['total_hours']} hours this week",
                'action': 'Consider delegating or rescheduling some tasks'
            })
        
        return recommendations
    
    def create_automation_rule(self, name: str, trigger: Dict, action: Dict) -> str:
        """Create an automation rule"""
        rule = {
            'id': f"RULE-{len(self.automation_rules) + 1:03d}",
            'name': name,
            'trigger': trigger,
            'action': action,
            'created_date': datetime.now().isoformat(),
            'active': True,
            'execution_count': 0
        }
        
        self.automation_rules.append(rule)
        return rule['id']
    
    def automate_email_responses(self, email_type: str, template_data: Dict) -> str:
        """Automate email response generation"""
        templates = {
            'task_assignment': {
                'subject': "New Task Assigned: {task_title}",
                'body': """
                Hi {assignee},
                
                You have been assigned a new task:
                
                Task: {task_title}
                Description: {task_description}
                Priority: {priority}
                Due Date: {due_date}
                
                Please confirm receipt and let us know if you have any questions.
                
                Best regards,
                Task Management System
                """
            },
            'task_reminder': {
                'subject': "Reminder: Task Due Soon - {task_title}",
                'body': """
                Hi {assignee},
                
                This is a reminder that the following task is due soon:
                
                Task: {task_title}
                Due Date: {due_date}
                Priority: {priority}
                
                Please update the task status or reach out if you need assistance.
                
                Best regards,
                Task Management System
                """
            },
            'task_completion': {
                'subject': "Task Completed: {task_title}",
                'body': """
                Hi Team,
                
                The following task has been completed:
                
                Task: {task_title}
                Completed by: {assignee}
                Completion Date: {completion_date}
                Duration: {actual_duration} minutes
                
                Great work!
                
                Best regards,
                Task Management System
                """
            }
        }
        
        if email_type not in templates:
            return "Email template not found"
        
        template = templates[email_type]
        
        try:
            subject = template['subject'].format(**template_data)
            body = template['body'].format(**template_data)
            
            email = {
                'id': f"EMAIL-{len(self.email_templates) + 1:04d}",
                'type': email_type,
                'subject': subject,
                'body': body,
                'generated_date': datetime.now().isoformat(),
                'sent': False
            }
            
            self.email_templates[email['id']] = email
            return email['id']
            
        except KeyError as e:
            return f"Missing template data: {e}"
    
    def optimize_calendar_scheduling(self, user: str, preferred_hours: tuple = (9, 17)) -> Dict:
        """Optimize calendar scheduling for a user"""
        user_tasks = [task for task in self.tasks.values() 
                     if task.assigned_to == user and task.status == TaskStatus.PENDING]
        
        # Sort tasks by priority and due date
        sorted_tasks = sorted(user_tasks, key=lambda t: (t.priority.value, t.due_date or datetime.max))
        
        # Generate optimized schedule
        schedule = []
        current_time = datetime.now().replace(hour=preferred_hours[0], minute=0, second=0, microsecond=0)
        
        for task in sorted_tasks:
            # Check if we need to move to next day
            if current_time.hour >= preferred_hours[1]:
                current_time = current_time.replace(hour=preferred_hours[0], minute=0) + timedelta(days=1)
            
            # Skip weekends
            while current_time.weekday() >= 5:  # Saturday = 5, Sunday = 6
                current_time += timedelta(days=1)
                current_time = current_time.replace(hour=preferred_hours[0], minute=0)
            
            # Schedule the task
            end_time = current_time + timedelta(minutes=task.estimated_duration)
            
            schedule.append({
                'task_id': task.id,
                'task_title': task.title,
                'start_time': current_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_minutes': task.estimated_duration,
                'priority': task.priority.name
            })
            
            # Move to next available slot (add 15-minute buffer)
            current_time = end_time + timedelta(minutes=15)
        
        optimization_result = {
            'user': user,
            'total_tasks': len(sorted_tasks),
            'total_duration_hours': sum(t.estimated_duration for t in sorted_tasks) / 60,
            'schedule': schedule,
            'optimization_tips': self._generate_scheduling_tips(user_tasks),
            'generated_date': datetime.now().isoformat()
        }
        
        return optimization_result
    
    def generate_productivity_report(self, user: str, period_days: int = 30) -> Dict:
        """Generate a productivity report for a user"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        user_tasks = [task for task in self.tasks.values() 
                     if task.assigned_to == user and task.created_date >= start_date]
        
        completed_tasks = [t for t in user_tasks if t.status == TaskStatus.COMPLETED]
        
        # Calculate metrics
        total_tasks = len(user_tasks)
        completion_rate = (len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
        
        # Average completion time
        completed_with_duration = [t for t in completed_tasks if t.actual_duration]
        avg_completion_time = (sum(t.actual_duration for t in completed_with_duration) / 
                              len(completed_with_duration)) if completed_with_duration else 0
        
        # Time estimation accuracy
        estimated_vs_actual = []
        for task in completed_with_duration:
            accuracy = min(task.estimated_duration / task.actual_duration, 2.0)  # Cap at 200%
            estimated_vs_actual.append(accuracy)
        
        estimation_accuracy = (sum(estimated_vs_actual) / len(estimated_vs_actual) * 100) if estimated_vs_actual else 0
        
        # Priority distribution
        priority_distribution = {
            'LOW': len([t for t in user_tasks if t.priority == Priority.LOW]),
            'MEDIUM': len([t for t in user_tasks if t.priority == Priority.MEDIUM]),
            'HIGH': len([t for t in user_tasks if t.priority == Priority.HIGH]),
            'URGENT': len([t for t in user_tasks if t.priority == Priority.URGENT])
        }
        
        # Performance trends
        weekly_completion = self._calculate_weekly_completion(completed_tasks, period_days)
        
        report = {
            'user': user,
            'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            'summary': {
                'total_tasks': total_tasks,
                'completed_tasks': len(completed_tasks),
                'completion_rate': f"{completion_rate:.1f}%",
                'avg_completion_time_minutes': f"{avg_completion_time:.0f}",
                'estimation_accuracy': f"{estimation_accuracy:.1f}%"
            },
            'priority_distribution': priority_distribution,
            'weekly_completion_trend': weekly_completion,
            'insights': self._generate_productivity_insights(user_tasks, completed_tasks),
            'recommendations': self._generate_productivity_recommendations(user_tasks, completed_tasks),
            'generated_date': datetime.now().isoformat()
        }
        
        self.reports.append(report)
        return report
    
    def automate_workflow(self, workflow_name: str, steps: List[Dict]) -> str:
        """Create and execute an automated workflow"""
        workflow_id = f"WORKFLOW-{len(self.workflows) + 1:03d}"
        
        workflow = {
            'id': workflow_id,
            'name': workflow_name,
            'steps': steps,
            'status': 'created',
            'created_date': datetime.now().isoformat(),
            'execution_log': []
        }
        
        self.workflows[workflow_id] = workflow
        
        # Execute workflow
        self._execute_workflow(workflow_id)
        
        return workflow_id
    
    def _trigger_automation_rules(self, task_id: str, old_status: TaskStatus, new_status: TaskStatus):
        """Trigger automation rules based on task status change"""
        for rule in self.automation_rules:
            if not rule['active']:
                continue
            
            trigger = rule['trigger']
            
            # Check if rule should be triggered
            should_trigger = False
            
            if trigger['type'] == 'status_change':
                if (trigger.get('from_status') == old_status.value and 
                    trigger.get('to_status') == new_status.value):
                    should_trigger = True
            elif trigger['type'] == 'task_completed':
                if new_status == TaskStatus.COMPLETED:
                    should_trigger = True
            elif trigger['type'] == 'task_overdue':
                task = self.tasks[task_id]
                if (task.due_date and task.due_date < datetime.now() and 
                    new_status != TaskStatus.COMPLETED):
                    should_trigger = True
            
            if should_trigger:
                self._execute_automation_action(rule, task_id)
                rule['execution_count'] += 1
    
    def _execute_automation_action(self, rule: Dict, task_id: str):
        """Execute an automation action"""
        action = rule['action']
        task = self.tasks[task_id]
        
        if action['type'] == 'send_email':
            template_data = {
                'task_title': task.title,
                'task_description': task.description,
                'assignee': task.assigned_to,
                'priority': task.priority.name,
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else 'Not set',
                'completion_date': task.completed_date.strftime('%Y-%m-%d') if task.completed_date else '',
                'actual_duration': task.actual_duration or 0
            }
            
            email_id = self.automate_email_responses(action['template'], template_data)
            
        elif action['type'] == 'create_task':
            self.create_task(
                title=action['title'].format(original_task=task.title),
                description=action['description'],
                priority=Priority[action['priority']],
                assigned_to=action['assigned_to']
            )
        
        elif action['type'] == 'update_status':
            if action.get('target_task_id'):
                self.update_task_status(action['target_task_id'], TaskStatus[action['status']])
    
    def _get_ready_tasks(self, user: str) -> List[Task]:
        """Get tasks that are ready to start (dependencies completed)"""
        user_tasks = [task for task in self.tasks.values() 
                     if task.assigned_to == user and task.status == TaskStatus.PENDING]
        
        ready_tasks = []
        for task in user_tasks:
            if not task.dependencies:
                ready_tasks.append(task)
            else:
                dependencies_completed = all(
                    self.tasks.get(dep_id, Task('', '', '', Priority.LOW, TaskStatus.FAILED, '', datetime.now(), None, None, [], [], 0, None)).status == TaskStatus.COMPLETED
                    for dep_id in task.dependencies
                )
                if dependencies_completed:
                    ready_tasks.append(task)
        
        return ready_tasks
    
    def _calculate_user_workload(self, user: str) -> Dict:
        """Calculate user workload for the current week"""
        start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
        end_of_week = start_of_week + timedelta(days=7)
        
        user_tasks = [task for task in self.tasks.values() 
                     if task.assigned_to == user and task.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]]
        
        total_minutes = sum(task.estimated_duration for task in user_tasks)
        total_hours = total_minutes / 60
        
        return {
            'total_hours': total_hours,
            'total_tasks': len(user_tasks),
            'week_start': start_of_week.strftime('%Y-%m-%d'),
            'week_end': end_of_week.strftime('%Y-%m-%d')
        }
    
    def _generate_scheduling_tips(self, tasks: List[Task]) -> List[str]:
        """Generate scheduling optimization tips"""
        tips = []
        
        if len(tasks) > 10:
            tips.append("Consider breaking down large tasks into smaller, manageable chunks")
        
        high_priority_count = len([t for t in tasks if t.priority in [Priority.HIGH, Priority.URGENT]])
        if high_priority_count > 5:
            tips.append("You have many high-priority tasks. Consider delegating some if possible")
        
        total_duration = sum(t.estimated_duration for t in tasks)
        if total_duration > 2400:  # 40 hours
            tips.append("Your task load exceeds 40 hours. Consider extending deadlines or redistributing work")
        
        return tips
    
    def _calculate_weekly_completion(self, completed_tasks: List[Task], period_days: int) -> List[Dict]:
        """Calculate weekly completion trends"""
        weeks = []
        end_date = datetime.now()
        
        for week in range(min(4, period_days // 7)):  # Show up to 4 weeks
            week_start = end_date - timedelta(days=(week + 1) * 7)
            week_end = end_date - timedelta(days=week * 7)
            
            week_tasks = [t for t in completed_tasks 
                         if week_start <= t.completed_date <= week_end]
            
            weeks.append({
                'week': f"Week {week + 1}",
                'completed_tasks': len(week_tasks),
                'total_duration': sum(t.actual_duration or 0 for t in week_tasks)
            })
        
        return list(reversed(weeks))
    
    def _generate_productivity_insights(self, all_tasks: List[Task], completed_tasks: List[Task]) -> List[str]:
        """Generate productivity insights"""
        insights = []
        
        if len(completed_tasks) > 0:
            completion_rate = len(completed_tasks) / len(all_tasks) * 100
            if completion_rate > 80:
                insights.append("🎯 Excellent completion rate! You're very productive.")
            elif completion_rate > 60:
                insights.append("👍 Good completion rate. Room for improvement.")
            else:
                insights.append("⚠️ Low completion rate. Consider reviewing task priorities.")
        
        # Analyze overdue tasks
        overdue_tasks = [t for t in all_tasks if t.due_date and t.due_date < datetime.now() and t.status != TaskStatus.COMPLETED]
        if len(overdue_tasks) > 0:
            insights.append(f"📅 You have {len(overdue_tasks)} overdue tasks requiring attention.")
        
        # Analyze priority distribution
        high_priority = len([t for t in all_tasks if t.priority in [Priority.HIGH, Priority.URGENT]])
        if high_priority > len(all_tasks) * 0.5:
            insights.append("🔥 More than 50% of your tasks are high priority. Consider better prioritization.")
        
        return insights
    
    def _generate_productivity_recommendations(self, all_tasks: List[Task], completed_tasks: List[Task]) -> List[str]:
        """Generate productivity recommendations"""
        recommendations = []
        
        # Time estimation recommendations
        completed_with_duration = [t for t in completed_tasks if t.actual_duration and t.estimated_duration]
        if completed_with_duration:
            over_estimated = len([t for t in completed_with_duration if t.actual_duration < t.estimated_duration * 0.8])
            under_estimated = len([t for t in completed_with_duration if t.actual_duration > t.estimated_duration * 1.2])
            
            if over_estimated > under_estimated:
                recommendations.append("⏱️ You tend to overestimate task duration. Try reducing time estimates.")
            elif under_estimated > over_estimated:
                recommendations.append("⏰ You tend to underestimate task duration. Add buffer time to estimates.")
        
        # Priority management recommendations
        pending_urgent = len([t for t in all_tasks if t.priority == Priority.URGENT and t.status == TaskStatus.PENDING])
        if pending_urgent > 0:
            recommendations.append("🚨 Focus on urgent tasks first to avoid bottlenecks.")
        
        # Workload management
        if len(all_tasks) > 20:
            recommendations.append("📋 Consider using task batching for similar activities to improve efficiency.")
        
        return recommendations
    
    def _execute_workflow(self, workflow_id: str):
        """Execute a workflow"""
        workflow = self.workflows[workflow_id]
        workflow['status'] = 'executing'
        
        for i, step in enumerate(workflow['steps']):
            try:
                # Simulate step execution
                step_result = self._execute_workflow_step(step)
                
                workflow['execution_log'].append({
                    'step': i + 1,
                    'description': step['description'],
                    'status': 'completed',
                    'result': step_result,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                workflow['execution_log'].append({
                    'step': i + 1,
                    'description': step['description'],
                    'status': 'failed',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                workflow['status'] = 'failed'
                return
        
        workflow['status'] = 'completed'
    
    def _execute_workflow_step(self, step: Dict) -> str:
        """Execute a single workflow step"""
        step_type = step['type']
        
        if step_type == 'create_task':
            task_id = self.create_task(
                title=step['title'],
                description=step['description'],
                priority=Priority[step['priority']],
                assigned_to=step['assigned_to']
            )
            return f"Created task: {task_id}"
        
        elif step_type == 'send_notification':
            # Simulate sending notification
            return f"Notification sent to {step['recipient']}"
        
        elif step_type == 'generate_report':
            # Simulate report generation
            return f"Report generated: {step['report_type']}"
        
        else:
            return f"Step type {step_type} executed successfully"

# Example usage and demonstration
def demonstrate_automation_agent():
    """Demonstrate the capabilities of the Automation Agent"""
    print("⚙️ Task Automation Agent Demonstration")
    print("=" * 50)
    
    # Initialize agent
    agent = AutomationAgent()
    
    # Create sample tasks
    print("\n1. Creating sample tasks...")
    task1 = agent.create_task(
        title="Develop new feature",
        description="Implement user authentication system",
        priority=Priority.HIGH,
        assigned_to="john.doe",
        due_date=datetime.now() + timedelta(days=7),
        tags=["development", "authentication"],
        estimated_duration=480  # 8 hours
    )
    
    task2 = agent.create_task(
        title="Write documentation",
        description="Create user guide for new feature",
        priority=Priority.MEDIUM,
        assigned_to="jane.smith",
        dependencies=[task1],
        estimated_duration=240  # 4 hours
    )
    
    print(f"Created tasks: {task1}, {task2}")
    
    # Create automation rule
    print("\n2. Creating automation rule...")
    rule_id = agent.create_automation_rule(
        name="Task completion notification",
        trigger={"type": "task_completed"},
        action={
            "type": "send_email",
            "template": "task_completion"
        }
    )
    print(f"Created automation rule: {rule_id}")
    
    # Update task status to trigger automation
    print("\n3. Completing task and triggering automation...")
    agent.update_task_status(task1, TaskStatus.COMPLETED)
    print("Task completed and automation triggered")
    
    # Get task recommendations
    print("\n4. Getting task recommendations...")
    recommendations = agent.get_task_recommendations("jane.smith")
    for rec in recommendations:
        print(f"   {rec['type']}: {rec['message']}")
    
    # Optimize calendar
    print("\n5. Optimizing calendar schedule...")
    schedule = agent.optimize_calendar_scheduling("jane.smith")
    print(f"Optimized schedule for {schedule['total_tasks']} tasks")
    print(f"Total duration: {schedule['total_duration_hours']:.1f} hours")
    
    # Generate productivity report
    print("\n6. Generating productivity report...")
    report = agent.generate_productivity_report("john.doe")
    print(f"Completion rate: {report['summary']['completion_rate']}")
    print(f"Insights: {len(report['insights'])}")
    print(f"Recommendations: {len(report['recommendations'])}")
    
    # Create and execute workflow
    print("\n7. Creating and executing workflow...")
    workflow_steps = [
        {
            "type": "create_task",
            "description": "Create project setup task",
            "title": "Project Setup",
            "description": "Initialize project structure",
            "priority": "MEDIUM",
            "assigned_to": "team.lead"
        },
        {
            "type": "send_notification",
            "description": "Notify team about new project",
            "recipient": "development.team"
        },
        {
            "type": "generate_report",
            "description": "Generate project kickoff report",
            "report_type": "project_kickoff"
        }
    ]
    
    workflow_id = agent.automate_workflow("Project Kickoff", workflow_steps)
    print(f"Workflow created and executed: {workflow_id}")
    
    # Display summary
    print("\n8. Summary:")
    print(f"   Total tasks: {len(agent.tasks)}")
    print(f"   Total workflows: {len(agent.workflows)}")
    print(f"   Automation rules: {len(agent.automation_rules)}")
    print(f"   Email templates: {len(agent.email_templates)}")

if __name__ == "__main__":
    demonstrate_automation_agent()
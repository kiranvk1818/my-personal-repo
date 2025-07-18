"""
Business Analytics Agent Example
Demonstrates data analysis and business intelligence capabilities
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

class BusinessAnalyticsAgent:
    """
    An AI agent that performs business analytics tasks including:
    - Sales performance analysis
    - Customer segmentation
    - Trend identification
    - KPI calculation and reporting
    """
    
    def __init__(self):
        self.data = None
        self.insights = []
    
    def load_sample_data(self):
        """Generate sample business data for demonstration"""
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
        
        # Generate sample sales data
        base_sales = 1000
        seasonal_factor = np.sin(2 * np.pi * np.arange(len(dates)) / 365) * 200
        trend_factor = np.arange(len(dates)) * 0.5
        noise = np.random.normal(0, 100, len(dates))
        
        sales = base_sales + seasonal_factor + trend_factor + noise
        sales = np.maximum(sales, 0)  # Ensure no negative sales
        
        self.data = pd.DataFrame({
            'date': dates,
            'sales': sales,
            'customers': np.random.poisson(50, len(dates)),
            'product_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], len(dates)),
            'region': np.random.choice(['North', 'South', 'East', 'West'], len(dates))
        })
        
        return "Sample business data loaded successfully!"
    
    def analyze_sales_performance(self):
        """Analyze sales performance and identify trends"""
        if self.data is None:
            return "No data loaded. Please load data first."
        
        # Calculate key metrics
        total_sales = self.data['sales'].sum()
        avg_daily_sales = self.data['sales'].mean()
        sales_growth = self.calculate_growth_rate()
        
        # Identify best and worst performing periods
        monthly_sales = self.data.groupby(self.data['date'].dt.to_period('M'))['sales'].sum()
        best_month = monthly_sales.idxmax()
        worst_month = monthly_sales.idxmin()
        
        insights = {
            'total_sales': f"${total_sales:,.2f}",
            'avg_daily_sales': f"${avg_daily_sales:,.2f}",
            'sales_growth': f"{sales_growth:.2f}%",
            'best_month': str(best_month),
            'worst_month': str(worst_month),
            'best_month_sales': f"${monthly_sales[best_month]:,.2f}",
            'worst_month_sales': f"${monthly_sales[worst_month]:,.2f}"
        }
        
        self.insights.append(("Sales Performance Analysis", insights))
        return insights
    
    def calculate_growth_rate(self):
        """Calculate year-over-year growth rate"""
        # Compare last 30 days with previous 30 days
        recent_sales = self.data.tail(30)['sales'].sum()
        previous_sales = self.data.iloc[-60:-30]['sales'].sum()
        
        if previous_sales > 0:
            growth_rate = ((recent_sales - previous_sales) / previous_sales) * 100
        else:
            growth_rate = 0
        
        return growth_rate
    
    def segment_customers(self):
        """Perform customer segmentation analysis"""
        # Group by region and calculate metrics
        regional_analysis = self.data.groupby('region').agg({
            'sales': ['sum', 'mean'],
            'customers': ['sum', 'mean']
        }).round(2)
        
        regional_analysis.columns = ['Total Sales', 'Avg Sales', 'Total Customers', 'Avg Customers']
        
        # Calculate customer value per region
        regional_analysis['Customer Value'] = (
            regional_analysis['Total Sales'] / regional_analysis['Total Customers']
        ).round(2)
        
        self.insights.append(("Customer Segmentation", regional_analysis.to_dict()))
        return regional_analysis
    
    def product_performance_analysis(self):
        """Analyze performance by product category"""
        product_analysis = self.data.groupby('product_category').agg({
            'sales': ['sum', 'mean', 'count']
        }).round(2)
        
        product_analysis.columns = ['Total Sales', 'Avg Sales', 'Transaction Count']
        
        # Calculate market share
        total_sales = self.data['sales'].sum()
        product_analysis['Market Share %'] = (
            (product_analysis['Total Sales'] / total_sales) * 100
        ).round(2)
        
        self.insights.append(("Product Performance", product_analysis.to_dict()))
        return product_analysis
    
    def generate_recommendations(self):
        """Generate business recommendations based on analysis"""
        recommendations = []
        
        # Analyze recent trends
        recent_trend = self.data.tail(30)['sales'].mean() - self.data.head(30)['sales'].mean()
        
        if recent_trend > 0:
            recommendations.append("✅ Sales trend is positive. Consider increasing marketing budget.")
        else:
            recommendations.append("⚠️ Sales trend is declining. Review pricing and promotional strategies.")
        
        # Regional recommendations
        regional_data = self.data.groupby('region')['sales'].sum()
        top_region = regional_data.idxmax()
        recommendations.append(f"🎯 Focus expansion efforts on the {top_region} region (highest sales).")
        
        # Product recommendations
        product_data = self.data.groupby('product_category')['sales'].sum()
        top_product = product_data.idxmax()
        recommendations.append(f"📈 Increase inventory for {top_product} category (top performer).")
        
        self.insights.append(("Recommendations", recommendations))
        return recommendations
    
    def create_dashboard_data(self):
        """Prepare data for dashboard visualization"""
        dashboard_data = {
            'daily_sales': self.data.set_index('date')['sales'].resample('D').sum(),
            'monthly_trends': self.data.set_index('date')['sales'].resample('M').sum(),
            'regional_breakdown': self.data.groupby('region')['sales'].sum(),
            'product_breakdown': self.data.groupby('product_category')['sales'].sum()
        }
        
        return dashboard_data
    
    def generate_executive_summary(self):
        """Generate an executive summary report"""
        if not self.insights:
            return "No analysis performed yet. Please run analysis methods first."
        
        summary = f"""
        📊 EXECUTIVE SUMMARY - Business Performance Report
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        KEY PERFORMANCE INDICATORS:
        """
        
        for insight_type, data in self.insights:
            summary += f"\n\n{insight_type.upper()}:\n"
            if isinstance(data, dict):
                for key, value in data.items():
                    summary += f"  • {key}: {value}\n"
            elif isinstance(data, list):
                for item in data:
                    summary += f"  • {item}\n"
        
        return summary

# Example usage and demonstration
def demonstrate_business_agent():
    """Demonstrate the capabilities of the Business Analytics Agent"""
    print("🤖 Business Analytics Agent Demonstration")
    print("=" * 50)
    
    # Initialize agent
    agent = BusinessAnalyticsAgent()
    
    # Load sample data
    print("\n1. Loading sample business data...")
    print(agent.load_sample_data())
    
    # Perform sales analysis
    print("\n2. Analyzing sales performance...")
    sales_insights = agent.analyze_sales_performance()
    for key, value in sales_insights.items():
        print(f"   {key}: {value}")
    
    # Customer segmentation
    print("\n3. Performing customer segmentation...")
    customer_segments = agent.segment_customers()
    print(customer_segments)
    
    # Product analysis
    print("\n4. Analyzing product performance...")
    product_performance = agent.product_performance_analysis()
    print(product_performance)
    
    # Generate recommendations
    print("\n5. Generating business recommendations...")
    recommendations = agent.generate_recommendations()
    for rec in recommendations:
        print(f"   {rec}")
    
    # Executive summary
    print("\n6. Executive Summary:")
    print(agent.generate_executive_summary())

if __name__ == "__main__":
    demonstrate_business_agent()
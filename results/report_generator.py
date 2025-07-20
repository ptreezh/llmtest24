"""
Report Generator for creating comprehensive test reports
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generates comprehensive reports from test results"""
    
    def __init__(self, config):
        """Initialize report generator"""
        self.config = config
        
    def generate_comprehensive_report(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        report = {
            'report_metadata': self._generate_metadata(),
            'executive_summary': self._generate_executive_summary(test_results),
            'detailed_analysis': self._generate_detailed_analysis(test_results),
            'recommendations': self._generate_recommendations(test_results),
            'appendices': self._generate_appendices(test_results)
        }
        
        return report
    
    def generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML report"""
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>LLM Role Independence Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
                .section { margin: 20px 0; }
                .score { font-weight: bold; color: #2e7d32; }
                .warning { color: #d32f2f; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>LLM Role Independence Test Report</h1>
                <p>Generated: {timestamp}</p>
                <p>Session ID: {session_id}</p>
            </div>
            
            <div class="section">
                <h2>Executive Summary</h2>
                {executive_summary}
            </div>
            
            <div class="section">
                <h2>Test Results</h2>
                {test_results_table}
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
                {recommendations}
            </div>
        </body>
        </html>
        """
        
        # Format the template with actual data
        formatted_html = html_template.format(
            timestamp=report_data['report_metadata']['generated_at'],
            session_id=report_data['report_metadata'].get('session_id', 'N/A'),
            executive_summary=self._format_executive_summary_html(report_data['executive_summary']),
            test_results_table=self._format_results_table_html(report_data['detailed_analysis']),
            recommendations=self._format_recommendations_html(report_data['recommendations'])
        )
        
        return formatted_html
    
    def _generate_metadata(self) -> Dict[str, Any]:
        """Generate report metadata"""
        
        return {
            'generated_at': datetime.now().isoformat(),
            'generator_version': '1.0.0',
            'report_type': 'comprehensive_analysis'
        }
    
    def _generate_executive_summary(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary"""
        
        summary = {
            'overall_assessment': 'pending',
            'key_findings': [],
            'critical_issues': [],
            'performance_highlights': []
        }
        
        # Analyze overall performance
        if 'test_results' in test_results:
            model_results = test_results['test_results']
            
            # Calculate average scores across models
            all_scores = []
            for model_name, model_data in model_results.items():
                if isinstance(model_data, dict):
                    # Extract scores from different test types
                    for test_type, test_data in model_data.items():
                        if isinstance(test_data, dict) and 'score' in test_data:
                            all_scores.append(test_data['score'])
            
            if all_scores:
                avg_score = sum(all_scores) / len(all_scores)
                
                if avg_score >= 0.8:
                    summary['overall_assessment'] = 'excellent'
                    summary['performance_highlights'].append(f"Outstanding performance with average score of {avg_score:.3f}")
                elif avg_score >= 0.7:
                    summary['overall_assessment'] = 'good'
                    summary['key_findings'].append(f"Good performance with average score of {avg_score:.3f}")
                elif avg_score >= 0.6:
                    summary['overall_assessment'] = 'fair'
                    summary['key_findings'].append(f"Fair performance with average score of {avg_score:.3f}")
                else:
                    summary['overall_assessment'] = 'needs_improvement'
                    summary['critical_issues'].append(f"Below average performance with score of {avg_score:.3f}")
        
        return summary
    
    def _generate_detailed_analysis(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed analysis"""
        
        analysis = {
            'model_performance': {},
            'test_type_analysis': {},
            'consistency_analysis': {},
            'independence_analysis': {}
        }
        
        if 'test_results' in test_results:
            model_results = test_results['test_results']
            
            for model_name, model_data in model_results.items():
                analysis['model_performance'][model_name] = self._analyze_model_performance(model_data)
        
        return analysis
    
    def _generate_recommendations(self, test_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on test results"""
        
        recommendations = []
        
        # Analyze results and generate specific recommendations
        if 'test_results' in test_results:
            model_results = test_results['test_results']
            
            for model_name, model_data in model_results.items():
                model_recommendations = self._generate_model_recommendations(model_name, model_data)
                recommendations.extend(model_recommendations)
        
        # Add general recommendations
        general_recommendations = [
            {
                'category': 'general',
                'priority': 'medium',
                'title': 'Regular Testing',
                'description': '建议定期进行角色独立性测试以监控模型性能变化。',
                'implementation': '每月进行一次完整的测试套件运行。'
            },
            {
                'category': 'general',
                'priority': 'low',
                'title': 'Test Coverage Expansion',
                'description': '考虑扩展测试场景以覆盖更多角色类型和应用场景。',
                'implementation': '逐步增加新的测试用例和角色定义。'
            }
        ]
        
        recommendations.extend(general_recommendations)
        
        return recommendations
    
    def _generate_appendices(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report appendices"""
        
        appendices = {
            'raw_data': test_results,
            'test_configuration': self.config.config if hasattr(self.config, 'config') else {},
            'methodology': {
                'description': '本报告基于统一LLM角色独立性测试框架生成',
                'test_types': [
                    'Character Breaking Test - 角色破坏测试',
                    'Implicit Cognition Test - 隐式认知测试', 
                    'Longitudinal Consistency Test - 纵向一致性测试'
                ],
                'scoring_methodology': '各项测试采用0-1评分制，1表示最佳性能'
            }
        }
        
        return appendices
    
    def _analyze_model_performance(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance for a specific model"""
        
        performance = {
            'overall_score': 0.0,
            'strengths': [],
            'weaknesses': [],
            'test_breakdown': {}
        }
        
        scores = []
        
        for test_type, test_data in model_data.items():
            if isinstance(test_data, dict):
                if 'score' in test_data:
                    score = test_data['score']
                    scores.append(score)
                    
                    performance['test_breakdown'][test_type] = {
                        'score': score,
                        'status': 'passed' if score >= 0.7 else 'failed',
                        'details': test_data
                    }
                    
                    # Identify strengths and weaknesses
                    if score >= 0.8:
                        performance['strengths'].append(f"{test_type}: {score:.3f}")
                    elif score < 0.6:
                        performance['weaknesses'].append(f"{test_type}: {score:.3f}")
        
        if scores:
            performance['overall_score'] = sum(scores) / len(scores)
        
        return performance
    
    def _generate_model_recommendations(self, model_name: str, model_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations for a specific model"""
        
        recommendations = []
        
        # Analyze model performance and generate specific recommendations
        for test_type, test_data in model_data.items():
            if isinstance(test_data, dict) and 'score' in test_data:
                score = test_data['score']
                
                if score < 0.6:
                    recommendations.append({
                        'category': 'performance',
                        'priority': 'high',
                        'model': model_name,
                        'test_type': test_type,
                        'title': f'{model_name} - {test_type} Performance Issue',
                        'description': f'{test_type}测试得分较低({score:.3f})，需要重点关注。',
                        'implementation': f'针对{test_type}进行专项优化和调整。'
                    })
                elif score < 0.7:
                    recommendations.append({
                        'category': 'improvement',
                        'priority': 'medium',
                        'model': model_name,
                        'test_type': test_type,
                        'title': f'{model_name} - {test_type} Improvement Opportunity',
                        'description': f'{test_type}测试有改进空间({score:.3f})。',
                        'implementation': f'考虑对{test_type}相关功能进行优化。'
                    })
        
        return recommendations
    
    def _format_executive_summary_html(self, summary: Dict[str, Any]) -> str:
        """Format executive summary for HTML"""
        
        html = f"<p><strong>Overall Assessment:</strong> {summary['overall_assessment']}</p>"
        
        if summary['key_findings']:
            html += "<h3>Key Findings:</h3><ul>"
            for finding in summary['key_findings']:
                html += f"<li>{finding}</li>"
            html += "</ul>"
        
        if summary['critical_issues']:
            html += "<h3>Critical Issues:</h3><ul>"
            for issue in summary['critical_issues']:
                html += f"<li class='warning'>{issue}</li>"
            html += "</ul>"
        
        if summary['performance_highlights']:
            html += "<h3>Performance Highlights:</h3><ul>"
            for highlight in summary['performance_highlights']:
                html += f"<li class='score'>{highlight}</li>"
            html += "</ul>"
        
        return html
    
    def _format_results_table_html(self, analysis: Dict[str, Any]) -> str:
        """Format results table for HTML"""
        
        html = "<table><tr><th>Model</th><th>Test Type</th><th>Score</th><th>Status</th></tr>"
        
        model_performance = analysis.get('model_performance', {})
        
        for model_name, performance in model_performance.items():
            test_breakdown = performance.get('test_breakdown', {})
            
            for test_type, test_info in test_breakdown.items():
                score = test_info['score']
                status = test_info['status']
                
                status_class = 'score' if status == 'passed' else 'warning'
                
                html += f"<tr><td>{model_name}</td><td>{test_type}</td><td class='{status_class}'>{score:.3f}</td><td>{status}</td></tr>"
        
        html += "</table>"
        
        return html
    
    def _format_recommendations_html(self, recommendations: List[Dict[str, Any]]) -> str:
        """Format recommendations for HTML"""
        
        html = "<ul>"
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_recommendations = sorted(recommendations, key=lambda x: priority_order.get(x['priority'], 3))
        
        for rec in sorted_recommendations:
            priority_class = 'warning' if rec['priority'] == 'high' else 'score' if rec['priority'] == 'medium' else ''
            
            html += f"<li class='{priority_class}'>"
            html += f"<strong>[{rec['priority'].upper()}] {rec['title']}</strong><br>"
            html += f"{rec['description']}<br>"
            html += f"<em>Implementation: {rec['implementation']}</em>"
            html += "</li>"
        
        html += "</ul>"
        
        return html
    
    def save_report(self, report_data: Dict[str, Any], output_path: str, format_type: str = 'json'):
        """Save report to file"""
        
        if format_type == 'json':
            with open(f"{output_path}.json", 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        elif format_type == 'html':
            html_content = self.generate_html_report(report_data)
            with open(f"{output_path}.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        logger.info(f"Report saved to {output_path}.{format_type}")

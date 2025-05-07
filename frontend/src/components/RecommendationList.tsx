import React from 'react';

interface Recommendation {
    title: string;
    description: string;
}

interface RecommendationListProps {
    recommendations: Recommendation[];
}

const RecommendationList: React.FC<RecommendationListProps> = ({ recommendations }) => {
    if (recommendations.length === 0) {
        return null;
    }

    return (
        <div className="pt-6 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
            <h2 className="text-xl font-semibold">推荐结果</h2>
            <ul className="space-y-4">
                {recommendations.map((rec, index) => (
                    <li key={index} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                        <h3 className="font-medium text-indigo-600">{rec.title}</h3>
                        <p className="text-sm text-gray-600 mt-2">{rec.description}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default RecommendationList; 
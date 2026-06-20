import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

class MLAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.numeric_cols = []
        self._load_data()

    def _load_data(self):
        try:
            if self.file_path.endswith('.csv'):
                self.df = pd.read_csv(self.file_path)
            elif self.file_path.endswith('.xlsx'):
                self.df = pd.read_excel(self.file_path)
            
            if self.df is not None:
                # Identify numeric columns for ML
                self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        except Exception as e:
            raise ValueError(f"데이터 로드 실패: {str(e)}")

    def get_summary_stats(self):
        if self.df is None:
            return "데이터를 불러오지 못했습니다."
        
        summary = self.df.describe(include='all').to_string()
        return summary

    def run_anomaly_detection(self):
        """Runs Isolation Forest to find anomalies in numeric data."""
        if not self.numeric_cols or len(self.df) < 10:
            return None, "숫자형 데이터가 부족하여 이상치 탐지를 건너뜁니다."

        data_num = self.df[self.numeric_cols]
        # Impute missing values with mean
        imputer = SimpleImputer(strategy='mean')
        data_imputed = imputer.fit_transform(data_num)

        # Standardize
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_imputed)

        # Run Isolation Forest
        model = IsolationForest(contamination=0.05, random_state=42) # 5% assumed anomalies
        preds = model.fit_predict(data_scaled)
        
        # Add to dataframe
        result_df = self.df.copy()
        result_df['Anomaly'] = preds # -1 is anomaly, 1 is normal
        result_df['Anomaly_Label'] = result_df['Anomaly'].map({1: 'Normal', -1: 'Anomaly'})
        
        anomalies_count = (preds == -1).sum()
        
        # Create Plotly Chart (using first two numeric columns if available)
        fig = None
        if len(self.numeric_cols) >= 2:
            x_col = self.numeric_cols[0]
            y_col = self.numeric_cols[1]
            fig = px.scatter(
                result_df, x=x_col, y=y_col, 
                color='Anomaly_Label', 
                color_discrete_map={'Normal': '#2563eb', 'Anomaly': '#e11d48'},
                title=f"이상치 탐지 결과 (Isolation Forest) - {anomalies_count}건 발견"
            )
            fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        return {
            "df": result_df,
            "anomalies_count": anomalies_count,
            "fig": fig,
            "report": f"전체 {len(self.df)}개 데이터 중 {anomalies_count}개의 이상치(Anomaly)가 발견되었습니다."
        }

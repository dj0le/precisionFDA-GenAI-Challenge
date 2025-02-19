export interface Document {
	file_id: string;
	filename: string;
	upload_timestamp: string;
}

export type ToastType = 'info' | 'success' | 'error' | 'warning';

export interface ResponseMetadata {
	total_duration?: number;
}

export interface UsageMetadata {
	total_tokens?: number;
}

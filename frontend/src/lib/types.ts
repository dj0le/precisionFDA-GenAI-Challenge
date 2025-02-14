export interface Document {
	file_id: string;
	filename: string;
	upload_timestamp: string;
}

export type ToastType = 'info' | 'success' | 'error' | 'warning';
